<template>
    <div class="bw-page-container">
        <div class="contents">
            <section>
                <h1 class="bwh1" style="display:inline-block; vertical-align: middle; margin-top: 2rem;">{{
                    translations?.leaderboard?.pagetitle ? translations.leaderboard.pagetitle : "leaderboard.pagetitle"
                    }}
                </h1>
                <div class="igrica-container">
                <iframe  src="https://brucifer-igrica.vercel.app/" class="igrica-frame"></iframe>
                </div>
                <div class="leaderboard-table">
                    <div class="leaderboard-title">
                        <h1>{{ translations?.leaderboard?.placementTableTitle ?
                            translations.leaderboard.placementTableTitle :
                            "leaderboard.placementTableTitle" }}</h1>
                        <h1>{{ translations?.leaderboard?.nameTableTitle ? translations.leaderboard.nameTableTitle :
                            "leaderboard.nameTableTitle" }}</h1>
                        <h1>
                            {{ translations?.leaderboard?.scoreTableTitle ? translations.leaderboard.scoreTableTitle :
                                "leaderboard.scoreTableTitle" }}</h1>

                        <div class="leaderboard-items" v-for="(player, index) in leaderboardData" :key="player.id">
                            <h1>#{{ index + 1 }}</h1>
                            <h1>{{ player.name }}</h1>
                            <h1>{{ player.score }}</h1>

                        </div>
                    </div>

                </div>
            </section>
        </div>
        <Footer></Footer>
    </div>
</template>

<script>
import Footer from '@/components/NavbarAndFooter/Footer.vue'
import axios from 'axios';
import translationsStore from '@/store/translationsStore';
import visibilityStore from '@/store/visibilityStore';
import debounce from 'lodash/debounce';



export default {
    name: 'IgricaView',
    components: { Footer },
    mounted() {
        this.sendScoreToBackend = debounce(this.sendScoreToBackend, 500);

        this.fetchLeaderboardData();
        window.addEventListener("message", this.receiveScore);
    },
    data() {
        return {
            showContactForm: true,
            showHid: false,
            tbodyHigh: false,

            leaderboardData: [],


        }
    }, computed: {
        translations() {
            return translationsStore.state.translations;
        }
    },
    methods: {
        async fetchLeaderboardData() {
            try {
                const response = await axios.get(process.env.VUE_APP_BASE_URL + '/gameLeaderboard/?ordering=-score');
                this.leaderboardData = response.data.slice.slice(0, 20);;
            } catch (error) {
                console.error('Error fetching leaderboard data:', error);
            }
        },
        receiveScore(event) {
            if (event.data && event.data.score && event.data.mail && event.data.nickname) {
                this.sendScoreToBackend(event.data);
            }
        },
        async sendScoreToBackend(scoreData) {

            const response = await axios.get(process.env.VUE_APP_BASE_URL + '/gameLeaderboard/?search=' +
                scoreData.mail + '&search_fields=email');

            if (response.data.length > 0) {
                let user = response.data[0];
                if (user.score < scoreData.score) {
                    await axios.delete(process.env.VUE_APP_BASE_URL + '/gameLeaderboard/' + user.id + '/',
                        { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } });
                    await axios.post(process.env.VUE_APP_BASE_URL + '/gameLeaderboard/', {
                        name: scoreData.nickname,
                        email: scoreData.mail,
                        score: scoreData.score
                    }, {
                        auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS }
                    });
                } else {
                    await axios.put(process.env.VUE_APP_BASE_URL + '/gameLeaderboard/' + user.id + '/', {
                        name: scoreData.nickname
                    }, {
                        auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS }
                    });
                }
            } else {
                await axios.post(process.env.VUE_APP_BASE_URL + '/gameLeaderboard/', {
                    name: scoreData.nickname,
                    email: scoreData.mail,
                    score: scoreData.score
                }, {
                    auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS }
                });
            }

            this.fetchLeaderboardData();
        },
    },


    beforeDestroy() {
        window.removeEventListener("message", this.receiveScore);
    }
}
</script>

<style>
.igrica-container {
    background-color: rgba(0, 0, 0, 0.3);
    padding: 1%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.igrica-frame {
    height: 650px;
    width: 480px;
}

.leaderboard-table {
    width: 100%;
    background-color: rgba(0, 0, 0, 0.3);
    height: 100%;
    overflow: auto;
    padding: 10px;
    padding-top: 0px;
    padding-right: 0px;
}


.leaderboard-title {
    display: grid;
    grid-template-columns: 25% 50% 25%;
}

.leaderboard-title h1 {
    color: white;
    font-size: 24px;
    font-weight: 700;
    padding: 20px;
    padding-left: 10px;
    padding-bottom: 20px;

}

.leaderboard-items h1 {
    font-weight: 400;
    padding: 10px;

}

.leaderboard-items {
    display: grid;
    grid-template-columns: 25% 50% 25%;
    grid-column: span 4;

}

.disclamer-text {
    font-size: 20px;
    font-weight: 400;
}

@media screen and (max-width: 980px) {
    .leaderboard-title h1 {
        font-size: 24px;
    }

    .leaderboard-table {
        margin-top: 100px;
    }
}

@media screen and (max-width: 980px) {
    .leaderboard-title h1 {
        font-size: 14px;
    }

    .disclamer-text {
        font-size: 14px;
    }
}

@media screen and (max-width: 550px) {

    .bwh1.cj {
        font-size: 15px;
        width: 95%;
    }
}

@import url(../../bruciweb.css);
</style>