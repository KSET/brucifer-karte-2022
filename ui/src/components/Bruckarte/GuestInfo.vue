<template>
    <div class="guest-info">
        <div v-if="wasEntered" class="entered-banner">Već ušao</div>

        <div class="guest-grid">
            <label class="textfield">Ime</label>
            <input readonly class="inputfield" type="text" :value="guest?.name">

            <template v-if="hasGuest && !isSponsor">
                <label class="textfield">Prezime</label>
                <input readonly class="inputfield" type="text" :value="guest.surname">
            </template>

            <template v-if="isBrucos">
                <label class="textfield">JMBAG</label>
                <input readonly class="inputfield" type="text" :value="guest.jmbag">

                <label class="textfield">Karta</label>
                <span class="status-btn" :class="{ 'is-yes': guest.bought }">
                    <img v-if="guest.bought" class="va" src="../../assets/icons/yes-icon.svg" alt="Kupljena">
                    <img v-else class="va" src="../../assets/icons/no-icon.svg" alt="Nije kupljena">
                </span>
            </template>

            <label class="textfield">Ulaz</label>
            <button type="button" class="status-btn" :class="{ 'is-yes': guest?.entered }"
                :disabled="!hasGuest || saving" @click="guest.entered ? undoCheckIn() : checkIn()">
                <img v-if="guest?.entered" class="va" src="../../assets/icons/yes-icon.svg" alt="Ušao">
                <img v-else class="va" src="../../assets/icons/no-icon.svg" alt="Nije ušao">
            </button>

            <p v-if="error" class="error-text">{{ error }}</p>

            <template v-if="isBrucos">
                <label class="textfield">Potvrda</label>
                <span class="textfield conf-code">{{ guest.confCode }}</span>
            </template>
        </div>
    </div>
</template>

<script>
import { api } from "@/plugins/api";
import { isBrucos, isSponsor, REQUEST_TIMEOUT } from '@/utils/guestTags';

export default {
    name: 'GuestInfo',
    props: {
        guest: {
            type: Object,
            default: () => ({}),
        },
    },
    emits: ['updated'],
    data() {
        return {
            saving: false,
            error: '',
            // snapshot taken when a guest is opened, so toggling entry here doesn't raise the warning
            wasEntered: false,
        }
    },
    computed: {
        guestId() {
            return this.guest?.id;
        },
        hasGuest() {
            return !!this.guestId;
        },
        isBrucos() {
            return isBrucos(this.guest?.tag);
        },
        isSponsor() {
            return isSponsor(this.guest?.tag);
        },
    },
    watch: {
        guestId: {
            immediate: true,
            handler() {
                this.wasEntered = !!this.guest?.entered;
                this.error = '';
            },
        },
    },
    methods: {
        checkIn() {
            return this.postEntry('check-in');
        },
        undoCheckIn() {
            if (!window.confirm('Poništiti ulaz za ovog gosta?')) return;
            return this.postEntry('undo-check-in');
        },
        // the endpoints set entered instead of toggling it, so retrying after a timeout is safe
        async postEntry(action) {
            if (!this.hasGuest || this.saving) return;
            const guest = this.guest;
            this.saving = true;
            this.error = '';
            try {
                const { data } = await api.post(`/guests/${guest.id}/${action}/`, {}, { timeout: REQUEST_TIMEOUT });
                this.$emit('updated', data.guest);
            } catch (err) {
                if (err.response?.status === 409) {
                    // another door already let them in; show the server's state, not ours
                    this.$emit('updated', err.response.data.guest);
                    if (this.guestId === guest.id) this.wasEntered = true;
                } else if (this.guestId === guest.id) {
                    this.error = err.response
                        ? 'Spremanje ulaza nije uspjelo, pokušajte ponovno.'
                        : 'Nema veze – pokušajte ponovno.';
                }
            } finally {
                this.saving = false;
            }
        },
    }
}
</script>

<style scoped>
.guest-info {
    padding: 20px;
    text-align: left;
}

.guest-grid {
    display: grid;
    grid-template-columns: 25% 75%;
    row-gap: 25px;
    align-items: center;
}

.guest-grid .inputfield {
    width: 100%;
}

.entered-banner {
    margin-bottom: 20px;
    padding: 10px;
    border-radius: 6px;
    background-color: #c62828;
    color: white;
    font-family: "Montserrat";
    font-weight: 700;
    font-size: 20px;
    text-align: center;
}

.status-btn {
    box-sizing: border-box;
    width: 25%;
    background-color: white;
    border: 1px solid #000000;
    border-radius: 6px;
    text-align: center;
}

.status-btn.is-yes {
    background-color: #000000;
}

.error-text {
    grid-column: 1 / -1;
    margin: 0;
    color: #c62828;
    font-family: "Montserrat";
    font-size: 14px;
}

.conf-code {
    overflow-wrap: anywhere;
}

@media screen and (max-width: 550px) {
    .status-btn {
        width: 76px;
        height: 25px;
    }
}
</style>
