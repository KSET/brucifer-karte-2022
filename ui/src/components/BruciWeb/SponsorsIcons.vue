<template>
    <div v-if="SPONSORS_VISIBILITY == 1" class="sponsorsIcons">
        <div v-for="sponsor in sponsors" :key="sponsor.id" class="sponsorr">
            <a v-bind:href="sponsor.url" rel="noreferrer noopener" target="_blank">
                <div>
                    <img v-bind:src="sponsor.image">
                </div>
            </a>
        </div>
    </div>
</template>

<script>
import Footer from '@/components/NavbarAndFooter/Footer.vue'
import axios from 'axios'
import store from '@/store/visibilityStore'
export default {
    name: 'SpoonsorsIcons',
    components: { Footer },
    props: {
        msg: String
    },
    data() {
        return {
            sponsors: [],
            SPONSORS_VISIBILITY: store.state.SPONSORS_VISIBILITY
        }
    },
    mounted() {
        this.created();
    },
    methods: {
        created() {
            axios.get(process.env.VUE_APP_BASE_URL + '/sponsors/?ordering=order&search=1&search_fields=visible',)
                .then(response => {
                    this.sponsors = response.data;
                })
        }
    }
}
</script>


<style scoped>
.sponsorsIcons {
    position: absolute;
    border: 2px solid red;
    top: 97vh;
    right: 6vw;
    left: 35vw;

    display: grid;
    grid-template-columns: repeat(13, 5rem);
}

.image-container {
    position: relative;
}

.image-container .image-sizer {
    transition: padding-bottom .3s ease;
    will-change: padding-bottom;
}

.image-container .image-frame {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-repeat: no-repeat;
    background-position: center center;
    background-size: contain;
}

.sponsorr {
    border-radius: 18px;
    padding: 5px;
}

@media screen and (max-width: 1550px) {
    .sponsors {
        grid-template-columns: repeat(4, minmax(0, 1fr));
    }
}

@media screen and (max-width: 980px) {
    .sponsors {
        grid-template-columns: repeat(3, minmax(0, 1fr));
    }
}

@media screen and (max-width: 635px) {
    .sponsors {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }
}

@media screen and (max-width: 21.875rem) {
    .sponsors {
        grid-template-columns: repeat(1, minmax(0, 1fr));
    }
}
</style>