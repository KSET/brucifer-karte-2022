<template>
    <div class="bw-page-container">
        <div class="contents">
            <section>
                <h1 class="bwh1">{{
                    translations?.leaderboard?.pagetitle ? translations.leaderboard.pagetitle : "leaderboard.pagetitle"
                    }}
                </h1>
                <div class="igrica-container">
                <iframe  src="https://brucifer-igrica.vercel.app/" class="igrica-frame"></iframe>
                </div>
            </section>
        </div>
        <Footer></Footer>
    </div>
</template>

<script>
import Footer from '@/components/NavbarAndFooter/Footer.vue'
import translationsStore from '@/store/translationsStore';

export default {
    name: 'IgricaView',
    components: { Footer },
    computed: {
        translations() {
            return translationsStore.state.translations;
        }
    }
}
</script>

<style scoped>
.igrica-container {
    background-color: var(--bw-card-bg);
    padding: 1%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.igrica-frame {
    height: 650px;
    width: 480px;
}
</style>