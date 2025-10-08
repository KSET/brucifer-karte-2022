<template>
    <div>
        <div color="primary">
            <img style="height: 50px;" src="../../assets/icons/qr-code-icon.svg">

            <v-dialog style="max-width: 600px;" v-model="dialogCamera" activator="parent">
                <v-card>
                    <v-card-item>
                        <StreamBarcodeReader @decode="onDecode" @loaded="onLoaded"></StreamBarcodeReader>
                    </v-card-item>
                    <v-card-actions>
                        <v-btn color="primary" block @click="dialogCamera = false">Zatvori</v-btn>
                    </v-card-actions>
                </v-card>
            </v-dialog>
        </div>

        <v-dialog v-model="dialogGuest" activator="parent">
            <v-card>
                <div v-if="success == 'true'">
                    <GuestInfo :guest="guest"></GuestInfo>
                </div>
                <div v-else-if="success == 'not-in-db'">
                    <p class="error-text">
                        QR kod i konfirmacijski kod su okej, ali kod nije u bazi podataka,pokušajte ponovno očitati kod, ili
                        manualno unesite ime </p>
                </div>
                <div v-else-if="success == 'invalid-qr'">
                    <p class="error-text">
                        QR kod je očitan, ali ne sadrži kod za potvrdu koji bi trebao sadržavati, pokušajte ponovno očitati
                        kod, ili manualno unesite ime
                    </p>
                </div>
                <div v-else>
                    <p class="error-text">
                        Dogodila se nepoznata greška, javite se administratoru </p>
                </div>
                <div class="closeBtn" @click="dialogGuest = false">
                    Zatvori
                </div>
            </v-card>
        </v-dialog>
    </div>
</template>

<script>
import { api } from "@/plugins/api";
import { StreamBarcodeReader } from "vue-barcode-reader";
import QrcodeStream from 'vue-qrcode-reader'
import GuestInfo from "./GuestInfo.vue";
export default {
    name: 'MobileEntry',
    props: {
        msg: String
    },
    components: {
        QrcodeStream,
        StreamBarcodeReader,
        GuestInfo
    },
    data() {
        return {
            guest: '',

            success: '',

            dialogCamera: false,
            dialogGuest: false,

        }
    },
    created() {
        //this.onDecode("20133370-a03a-11ed-99c7-bd21e9b0b861")
    },
    methods: {
        onDecode(uuid) {
            if (this.checkUUID(uuid)) {
                api.get(process.env.VUE_APP_BASE_URL + '/guests/?search=Brucoši ' + uuid + "&search_fields=tag&search_fields=confCode",)
                    .then(response => {
                        if (response.data.length == 0) {
                            this.success = 'not-in-db'
                        } else {
                            this.guest = response.data[0]
                            this.success = 'true';
                        }

                    })
            } else {
                this.success = 'invalid-qr'
            }
            this.dialogGuest = true;
        },
        checkUUID(uuid) {
            const regexExp = /^[0-9A-F]{8}-[0-9A-F]{4}-[1][0-9A-F]{3}-[89AB][0-9A-F]{3}-[0-9A-F]{12}$/i;
            return regexExp.test(uuid);
        }
    }
}
</script>

<style scoped>
.closeBtn {
    width: 93%;
    text-align: center;
    height: 30px;
    border: 1px solid black;
    margin: -10px 10px 10px 10px;
    border-radius: 10px;
}

.error-text{
    height: 80px;
    color: black;
    padding: 2%;
}
</style>