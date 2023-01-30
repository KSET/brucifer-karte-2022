<template>
    <div>
        <StreamBarcodeReader @decode="onDecode" @loaded="onLoaded"></StreamBarcodeReader>
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

        }
    },
    created() {
    },
    methods: {
        onDecode(text) {
            if (this.checkUUID(text)) {
                axios.get(process.env.VUE_APP_BASE_URL + '/guests/?search=Brucoši ' + text + "&search_fields=tag&search_fields=confCode",)
                    .then(response => {
                        window.alert(response.data[0].name)
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