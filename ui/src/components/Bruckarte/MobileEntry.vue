<template>
    <div>
        <StreamBarcodeReader @decode="onDecode" @loaded="onLoaded"></StreamBarcodeReader>
    </div>
</template>

<script>
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
    methods: {
        onDecode(text) {
            window.alert(`Decode text from QR code is ${text}`)
            console.log(`Decode text from QR code is ${text}`)
        },
    }
}
</script>

<style>

</style>