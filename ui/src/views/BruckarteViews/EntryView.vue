<template>
    <div class="entry-view">
        <div class="entry-view__controls">
            <div class="entry-view__fields">
                <div class="entry-view__field">
                    <input class="nosubmit search" type="text" v-model="search" placeholder="Unesi Ime"
                        @input="onQueryChange" />
                    <button v-if="search" type="button" class="field-icon remove-icon" aria-label="Očisti pretragu"
                        @click="clearSearch"></button>
                </div>
                <div class="entry-view__qr">
                    <MobileEntry />
                </div>
                <div class="entry-view__field">
                    <select class="inputfield entry" v-model="selectedTag" @change="onQueryChange">
                        <option value="">Svi tagovi</option>
                        <option v-for="tag in tags" :key="tag" :value="tag">{{ tag }}</option>
                    </select>
                    <span class="field-icon dropdown-icon" aria-hidden="true"></span>
                </div>
            </div>
        </div>

        <div class="entry-view__list">
            <div v-if="loading" class="entry-view__status">
                <v-progress-circular size="90px" indeterminate color="black"></v-progress-circular>
            </div>
            <p v-else-if="error" class="entry-view__status entry-view__status--error">{{ error }}</p>
            <p v-else-if="searched && !guests.length" class="entry-view__status">Nema rezultata</p>
            <p v-if="hasMore" class="entry-view__more">Prikazano prvih {{ maxResults }} – upiši više slova</p>

            <button v-for="g in guests" :key="g.id" type="button" class="person"
                :class="{ 'person--selected': g.id === selectedGuest?.id }" @click="selectGuest(g)">
                <p><strong>{{ g.name }} {{ g.surname }}</strong></p>
                <p>{{ displayTag(g.tag) }}</p>
            </button>
        </div>

        <div class="entry-view__details">
            <GuestInfo :guest="selectedGuest" @updated="onGuestUpdated"></GuestInfo>
        </div>

        <!-- only displayed on mobile, where the details panel is hidden -->
        <div v-if="overlayOpen" class="entry-view__overlay" @click.self="overlayOpen = false">
            <div class="entry-view__overlay-card">
                <GuestInfo :guest="selectedGuest" @updated="onGuestUpdated"></GuestInfo>
                <button type="button" class="close-btn" @click="overlayOpen = false">Zatvori</button>
            </div>
        </div>
    </div>
</template>

<script>
import debounce from 'lodash/debounce';
import { api } from "@/plugins/api";
import GuestInfo from '@/components/Bruckarte/GuestInfo.vue';
import MobileEntry from '@/components/Bruckarte/MobileEntry.vue';
import { displayTag, REQUEST_TIMEOUT } from '@/utils/guestTags';

const MIN_QUERY_LENGTH = 3;
// a short query like "ana" can match hundreds of guests, too much to download on a slow phone
const MAX_RESULTS = 50;

export default {
    name: 'EntryView',
    components: {
        GuestInfo,
        MobileEntry
    },
    data() {
        return {
            tags: [],
            selectedTag: '',
            search: '',

            guests: [],
            hasMore: false,
            maxResults: MAX_RESULTS,
            selectedGuest: null,
            overlayOpen: false,

            loading: false,
            searched: false,
            error: '',
            searchSeq: 0,
            searchAbort: null,
        }
    },
    created() {
        this.runSearch = debounce(this.runSearch, 400);
        this.fetchTags();
    },
    beforeUnmount() {
        this.runSearch.cancel();
        this.searchSeq++;
        this.searchAbort?.abort();
    },
    methods: {
        displayTag,
        async fetchTags() {
            try {
                const { data } = await api.get('/tags/');
                this.tags = data.map(tag => tag.name);
            } catch (err) {
                this.error = 'Dohvaćanje tagova nije uspjelo.';
            }
        },
        onQueryChange() {
            // invalidate any in-flight search now, not when the debounce fires, so a slow
            // stale response can't fill the list or auto-open the wrong guest in between
            this.searchSeq++;
            // and drop its download, which would compete with the next search on a slow connection
            this.searchAbort?.abort();
            this.guests = [];
            this.hasMore = false;
            this.selectedGuest = null;
            this.overlayOpen = false;
            this.searched = false;
            this.error = '';

            if (this.search.trim().length < MIN_QUERY_LENGTH) {
                this.runSearch.cancel();
                this.loading = false;
                return;
            }
            this.loading = true;
            this.runSearch();
        },
        async runSearch() {
            const seq = ++this.searchSeq;
            this.searchAbort?.abort();
            const abort = new AbortController();
            this.searchAbort = abort;
            this.loading = true;
            const params = new URLSearchParams({ name_search: this.search.trim() });
            if (this.selectedTag) params.append('tag__icontains', this.selectedTag);
            params.append('limit', MAX_RESULTS + 1);
            try {
                const { data } = await api.get('/guests/', { params, timeout: REQUEST_TIMEOUT, signal: abort.signal });
                if (seq !== this.searchSeq) return;
                this.hasMore = data.length > MAX_RESULTS;
                this.guests = data.slice(0, MAX_RESULTS);
                this.searched = true;
                if (data.length === 1) this.selectGuest(data[0]);
            } catch (err) {
                if (seq === this.searchSeq) {
                    this.error = err.response ? 'Greška prilikom pretraživanja.' : 'Spora veza, pokušajte ponovno.';
                }
            } finally {
                if (seq === this.searchSeq) this.loading = false;
            }
        },
        clearSearch() {
            this.search = '';
            this.onQueryChange();
        },
        selectGuest(guest) {
            this.selectedGuest = guest;
            this.overlayOpen = true;
        },
        onGuestUpdated(updated) {
            const index = this.guests.findIndex(g => g.id === updated.id);
            if (index !== -1) this.guests.splice(index, 1, updated);
            if (this.selectedGuest?.id === updated.id) this.selectedGuest = updated;
        },
    }
}
</script>

<style lang="scss" scoped>
.entry-view {
    display: grid;
    grid-template-columns: auto 34.47%;
    grid-template-rows: auto 80.76%;
    grid-template-areas:
        "controls list"
        "details list";
    width: 100vw;
    height: 93vh;
}

.entry-view__controls {
    grid-area: controls;
    display: flex;
    align-items: center;
    padding: 20px;
    border-bottom: 1px solid #000000;
    font-size: 30px;
}

.entry-view__fields {
    display: grid;
    grid-template-columns: 50% 50%;
    width: 100%;
}

.entry-view__field {
    position: relative;
    width: 95%;
    padding: 10px 0;

    .nosubmit.search {
        width: 100%;
        left: 0;
        margin: 0;
    }
}

.entry-view__qr {
    grid-row: span 2;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 5px;
    border: 1px solid black;
    border-radius: 5px;
}

.field-icon {
    position: absolute;
    right: 10px;
    top: 55%;
    transform: translateY(-50%);
    width: 16px;
    height: 16px;
    padding: 0;
    border: 0;
    background-position: center;
    background-repeat: no-repeat;
    background-size: contain;
}

.remove-icon {
    background-image: url('../../assets/icons/remove-icon.svg');
    cursor: pointer;
}

.dropdown-icon {
    background-image: url('../../assets/icons/dopdwn-notopen-icon.svg');
    pointer-events: none;
}

.entry-view__list {
    grid-area: list;
    margin-right: 5px;
    border-left: 1px solid #000000;
    overflow: auto;
    font-size: 30px;
}

.entry-view__status {
    display: flex;
    justify-content: center;
    padding: 20px;
    font-family: "Montserrat";
    font-size: 16px;
}

.entry-view__status--error {
    color: #c62828;
}

.entry-view__more {
    position: sticky;
    top: 10px;
    z-index: 1;
    margin: 10px;
    padding: 10px;
    border-radius: 6px;
    background-color: #c62828;
    color: white;
    font-family: "Montserrat";
    font-weight: 700;
    font-size: 16px;
    text-align: center;
}

.person {
    display: block;
    width: 100%;
    box-sizing: border-box;
    background-color: white;
    border: 0;
    border-bottom: 1px solid #000000;

    &--selected {
        background-color: #D9D9D9;
    }

    p {
        font-size: 0.6em;
        font-family: "Montserrat";
        color: black;
    }
}

.entry-view__details {
    grid-area: details;
    font-size: 30px;
}

.entry-view__overlay {
    display: none;
    position: fixed;
    inset: 0;
    z-index: 100;
    align-items: center;
    justify-content: center;
    background-color: rgba(0, 0, 0, 0.5);
}

.entry-view__overlay-card {
    width: 80%;
    background-color: white;
    border-radius: 15px;
}

.close-btn {
    display: block;
    width: 93%;
    height: 30px;
    margin: -10px 10px 10px 10px;
    border: 1px solid black;
    border-radius: 10px;
    background-color: white;
    text-align: center;
}

@media screen and (max-width: 550px) {
    .entry-view {
        display: flex;
        flex-direction: column;
    }

    .entry-view__field {
        padding: 7px 0;

        .nosubmit.search {
            font-size: 12px;
        }
    }

    .entry-view__list {
        height: 100%;
        border-left: none;
    }

    .entry-view__details {
        display: none;
    }

    .entry-view__overlay {
        display: flex;
    }
}
</style>
