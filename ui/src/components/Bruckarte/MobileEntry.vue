<template>
    <div>
        <v-btn color="primary">
            OTVORI KAMERU

            <v-dialog v-model="dialogCamera" activator="parent" height="40rem" width="40rem">
                <v-card>
                    <v-card-item>
                        <StreamBarcodeReader @decode="onDecode" @loaded="onLoaded"></StreamBarcodeReader>
                    </v-card-item>
                    <v-card-actions>
                        <v-btn color="primary" block @click="dialogCamera = false">Zatvori</v-btn>
                    </v-card-actions>
                </v-card>
            </v-dialog>
        </v-btn>

        <v-dialog v-model="dialogGuest" activator="parent" height="40rem" width="40rem">
            <v-card>
                <v-card-text>
                    {{ this.name }}
                    {{ this.surname }}
                    {{ this.jmbag }}
                    {{ this.bought }}
                    {{ this.entered }}

                </v-card-text>
                <v-card-actions>
                    <v-btn color="primary" block @click="dialogGuest = false">Zatvori</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
    </div>
</template>

<script>
import axios from "axios";
import { StreamBarcodeReader } from "vue-barcode-reader";
import QrcodeStream from 'vue-qrcode-reader'
export default {
    name: 'MobileEntry',
    props: {
        msg: String
    },
    components: {
        QrcodeStream,
        StreamBarcodeReader
    },
    data() {
        return {
            guest: '',
            name: '',
            surname: '',
            jmbag: '',
            phone: '',
            tag: '',
            bought: '',
            entered: '',
            dialogCamera: false,
            dialogGuest: false,

        }
    },
    created() {
        this.onDecode("2002caa0-a038-11ed-8d7c-538c6843e2f4")
    },
    methods: {
        onDecode(text) {
            if (this.checkUUID(text)) {
                console.log("adsadsd")
                axios.get(process.env.VUE_APP_BASE_URL + '/guests/?search=Brucoši ' + text + "&search_fields=tag&search_fields=confCode",)
                    .then(response => {
                        this.guest = response.data[0]
                        this.name = this.guest.name;
                        this.id = this.guest.id;
                        this.bought = this.guest.bought;
                        this.entered = this.guest.entered;
                        this.surname = this.guest.surname;
                        this.jmbag = this.guest.jmbag;

                        this.dialogGuest = true;
                    })
            } else {
                window.alert("QR kod je očitan, ali ne sadrži kod za potvrdu koji bi trebao sadržavati, pokušajte ponovno očitati kodk, ili manualno unesite ime")
            }
        },
        checkUUID(text) {
            const regexExp = /^[0-9A-F]{8}-[0-9A-F]{4}-[1][0-9A-F]{3}-[89AB][0-9A-F]{3}-[0-9A-F]{12}$/i;
            return regexExp.test(text);
        }
    }
}
</script>

<style>

</style>