<template>
    <div class="footery">
        <p id="text1" class="footer-text"> © KSET {{ year }}</p>

        <div class="footer-left-container">
            <div v-if="IGRICA_VISIBILITY != 0">
                <router-link class="footer-text" to="/uvjeti-koristenja">
                    <p class="footer-text">Uvjeti korištenja</p>
                </router-link>
            </div>
            <router-link class="footer-text" style="margin-left:30px" to="/pravila-ponasanja">
                <p class="footer-text">Pravila ponašanja</p>
            </router-link>
        </div>
    </div>
</template>


<script>
import visibilityStore from '@/store/visibilityStore';

export default {
    name: "Footer",
    data() {
        return {
            year: new Date().getFullYear(),
        }
    },
    computed: {
        IGRICA_VISIBILITY() {
            return visibilityStore.state.IGRICA_VISIBILITY;
        }
    }
}

</script>

<style>
.footery {
    background-color: var(--bw-footer-color);
    position: absolute;
    padding: 0px;
    bottom: 0;
    width: 100%;
    height: 60px;
    position: absolute;
    /* background: var(--bw-footer-color);
; */
}

.footery::after {
    position: absolute;
    top: -8px;
    right: 0;
    left: 0;
    z-index: 2;
    height: 8px;
    content: "";
    /* background: linear-gradient(to top, var(--bw-footer-color);
, transparent); */
}

#text1 {
    position: absolute;
    left: 2.73%;
    top: 37.5%;
    bottom: 20%;
}

.footer-left-container {

    display: flex;
    position: absolute;

    right: 5.86%;
    top: 37.5%;
    bottom: 20%;

}

.footer-text {
    font-family: 'Ubuntu';
    font-style: normal;
    font-weight: 400;
    font-size: 14px;
    line-height: 14px;
    /* or 100% */

    text-align: right;
    letter-spacing: -0.022em;

    color: #FFFFFF;
}

.footer-text:hover {
    color: #dbe9f4;
}
</style>
