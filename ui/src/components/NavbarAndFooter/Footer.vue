<template>
    <div class="footery">
        <p id="text1"> © KSET {{year}}</p>

        <router-link id="text2" to="/pravila-ponasanja">
            Pravila ponašanja
        </router-link>

    </div>
</template>

<script>
export default {
    name: "Footer",
    data() {
        return {
            year: new Date().getFullYear(),
        }
    }
}

</script>

<style>
.footery {
    background-color: #0E315B;
    position: absolute;
    padding: 0px;
    bottom: 0;
    width: 100%;
    height: 60px;
    position: absolute;
    /* background: #0E315B;
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
    /* background: linear-gradient(to top, #0E315B;
, transparent); */
}

#text1 {
    position: absolute;
    left: 2.73%;
    right: 56.25%;
    top: 37.5%;
    bottom: 20%;

    font-family: 'Ubuntu';
    font-style: normal;
    font-weight: 400;
    font-size: 14px;
    line-height: 14px;
    /* or 100% */

    letter-spacing: -0.022em;

    color: #FFFFFF;
}

#text2 {
    position: absolute;

    right: 5.86%;
    top: 37.5%;
    bottom: 20%;

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
</style>
