<template>
    <div class="grid-item grid1-item3" :class="{ [$style.cFix]: true, [$style.cFixExpanded]: guest?.tag === 'Brucoši' }"
        id="c">
        <div class="grid-container3">
            <h1 class="textfield">Ime </h1>
            <input readonly class="inputfield " :disabled="guest?.id == ''" type="text" @input="changeValue"
                v-model="guest.name">

            <h1 v-if="guest?.tag !== undefined && !guest?.tag.includes('Sponzor')" class="textfield ">Prezime</h1>
            <input v-if="guest?.tag !== undefined && !guest?.tag.includes('Sponzor')" readonly class="inputfield "
                :disabled="guest?.id == ''" type="text" @input="changeValue" v-model="guest.surname">

            <h1 v-if="guest?.tag == 'Brucoši'" class="textfield ">JMBAG </h1>
            <input v-if="guest?.tag == 'Brucoši'" class="inputfield " readonly type="text" v-model="guest.jmbag">

            <h1 v-if="guest?.tag == 'Brucoši'" class="textfield">Karta </h1>

            <button disabled v-if="guest?.tag == 'Brucoši' && guest?.bought == '1'" class="bttn button2-yes"
                @click="changeBought(guest, '0')">
                <img class="va" src="../../assets/icons/yes-icon.svg">
            </button>
            <button disabled class="bttn button2-no" v-if="guest?.tag == 'Brucoši' && guest?.bought == '0'"
                @click="changeBought(guest, '1')">
                <img class="va" src="../../assets/icons/no-icon.svg">
            </button>
            <h1 class="textfield">Ulaz </h1>

            <button v-if="guest?.entered == '1'" type="button" :disabled="guest?.id == ''" class="bttn button2-yes"
                @click="changeEntered(guest, '0')">
                <img class="va" src="../../assets/icons/yes-icon.svg">
            </button>
            <button v-else @click="changeEntered(guest, '1')" :disabled="guest?.id == ''" type="button"
                class="bttn button2-no">
                <img class="va" src="../../assets/icons/no-icon.svg">
            </button>

            <h1 v-if="guest?.tag == 'Brucoši'" class="textfield">Potvrda </h1>
            <h1 v-if="guest?.tag == 'Brucoši'" class="textfield" style="width: 100%">{{ guest?.confCode }} </h1>
        </div>
    </div>
</template>



<script>
import axios from 'axios';
export default {
    name: 'GuestInfo',
    components: {

    },
    props: {
        guest: {
            type: Object,
            default: () => ({}),
        },
    },
    data() {
        return {
        }
    },
    methods: {
        changeEntered(guest, changenum) {
            axios.put(process.env.VUE_APP_BASE_URL + '/guests/' + guest.id + '/',
                { entered: changenum },
                { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } }
            )
                .then(() => {
                    this.guest.entered = changenum;
                })
        },
    }
}
</script>

<style module lang="scss">
.person {

    p {
        font-size: .6em;
        font-family: 'Montserrat';
    }
}



:global(#flex) .cFix {
    @media screen and (max-width: 550px) {
        display: flex !important;
        flex-direction: column;
        height: fit-content;
        justify-content: flex-start;

        &.cFixExpanded {
            height: 100%;
        }
    }
}
</style>

<style scoped>
.grid-container3 {
    display: grid;
    grid-template-columns: 25% 75%;
    row-gap: 25px;
    align-items: center;
}

.inputfield {
    width: 100%;
}

.grid1-container {
    display: grid;
    grid-template-columns: auto 34.47%;
    grid-template-rows: auto 80.76%;
    width: 100vw;
    height: 93vh;
}

.grid3-container {
    left: 6%;
    display: grid;
    grid-template-columns: 23.6% auto;
    padding: 10px;
    grid-gap: 6%;


}

.grid-item {
    padding: 20px;
    font-size: 30px;
    text-align: left;
}

.grid1-item1 {
    border-bottom: 1px solid #000000;
}

.grid1-item2 {
    border-left: 1px solid #000000;
    overflow: auto;
    margin-right: 5px;
}

.grid1-item3 {
    overflow: visible;
}

.inputfield {
    border: 1px solid;
    left: 6%;

}

#inputfield {
    width: 50.6%;
}

.nosubmit.search {
    position: relative;
    margin-top: 2.375rem;
    width: 20%;
    margin-left: 6%;
}

.person {
    display: block;
    width: 100%;
    box-sizing: border-box;
    background-color: white;
    border: 0px;
    border-bottom: 1px solid #000000 !important;
}

.menu-item {
    width: 35%;
}

.p {
    font-size: 16px;
}

.button2-yes {
    box-sizing: border-box;

    width: 25%;


    background: #000000;
    border: 1px solid #000000;
    border-radius: 6px;
}

.button2-no {
    box-sizing: border-box;
    width: 25%;

    background-color: white !important;
    border: 1px solid #000000;
    border-radius: 6px;

}

.va {
    margin-bottom: 5px;
}

.nosubmit.search.entry {
    width: 90%;
    left: 0px;
    margin: 0px;
}

.inputfield.entry {
    width: 90%;
}

.grid1-item {
    width: 50% !important;
    display: inline-block !important;

}

.grid-container2 {
    left: 6%;
    display: grid;
    grid-template-columns: 5% auto !important;
    padding: 10px;
    grid-gap: 15%;
    row-gap: 3rem;
    align-items: center;
}

.showMobile {
    display: none;
}

@media screen and (max-width: 980px) {
    .hideDesktop {
        display: inline-block !important;
    }

    .hideTablet {
        display: none;
    }

    .textfield {
        font-size: 14px;
    }

    .showMobile {
        display: none !important;
    }

}

@media screen and (max-width: 550px) {
    .grid1-container {
        display: block !important;
    }

    .grid1-container {
        display: block !important;
    }

    .grid3-container {
        display: block !important;


    }

    .grid-item {
        display: block !important;
    }

    .grid1-item1 {
        border-bottom: 1px solid #000000;
    }

    .grid1-item2 {
        display: block !important;
    }

    #flex {
        display: flex !important;
        flex-direction: column;
    }

    #a {
        order: 1;
    }

    #b {
        order: 3;
        height: 50%
    }

    #c {
        order: 2;
    }
}


@media screen and (max-width: 550px) {
    .grid1-item {
        display: inline-block !important;
        margin: 0px;
        padding: 0px;
        width: 50% !important;
    }

    .nosubmit.search.entry {
        width: 90% !important;
    }

    .inputfield.entry {
        width: 90% !important;
    }

    .grid1-item2 {
        border-left: none;

    }

    .textfield {
        font-size: 12px;
    }

    .bttn {
        width: 76px;
        height: 25px;
    }

    .va {
        width: 19px;
        height: 19px;
        margin-top: 3px;
        vertical-align: top;
    }

    .grid-container2 {
        left: 6%;
        display: grid;
        grid-template-columns: 5% 1% 5% 10% 30%;
        padding: 10px;
        padding-top: 3px;

        grid-gap: 15%;
        row-gap: 3rem;
        align-items: center;
    }

    .showMobile {
        display: block !important;
    }
}
</style>