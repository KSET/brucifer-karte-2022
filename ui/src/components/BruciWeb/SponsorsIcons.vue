<template>
    <div v-if="SPONSORS_VISIBILITY == 1" class="sponsorsIcons">
        <div v-for="sponsor in sponsors" :key="sponsor.id" class="sponsorsIcon">
            <a v-bind:href="sponsor.url" rel="noreferrer noopener" target="_blank">
                <div>
                    <img v-bind:src="sponsor.image">
                </div>
            </a>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import store from '@/store/visibilityStore'

export default {
    name: 'SpoonsorsIcons',
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
    top: 0px;
    padding-top: 36%;
    right: 3vw;
    display: grid;
    grid-template-columns: repeat(16, 4rem);
    align-items: center;
}

.sponsorsIcon {
    border-radius: 18px;
    padding: 5px;
}

@media screen and (max-width: 980px) {
    .sponsorsIcons {
        display: none;
    }
}

@media screen and (max-width: 1555px) {
    .sponsorsIcons {
        grid-template-columns: repeat(16, 3.5rem);
    }
}

@media screen and (max-width: 1350px) {
    .sponsorsIcons {
        grid-template-columns: repeat(16, 3rem);
    }
}

@media screen and (max-width: 1175px) {
    .sponsorsIcons {
        grid-template-columns: repeat(16, 2.5rem);
    }
}
</style>