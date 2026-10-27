<template>
    <div>
        <button type="button" class="qr-trigger" aria-label="Skeniraj QR kod" @click="cameraOpen = true">
            <img class="qr-icon" src="../../assets/icons/qr-code-icon.svg" alt="">
        </button>

        <v-dialog v-model="cameraOpen" max-width="600">
            <v-card>
                <v-card-item>
                    <!-- v-if so the camera is released as soon as the dialog closes -->
                    <StreamBarcodeReader v-if="cameraOpen" @decode="onDecode"></StreamBarcodeReader>
                </v-card-item>
                <v-card-actions>
                    <v-btn color="primary" block @click="cameraOpen = false">Zatvori</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>

        <v-dialog v-model="resultOpen">
            <v-card>
                <div v-if="lookingUp" class="lookup">
                    <v-progress-circular indeterminate color="black"></v-progress-circular>
                    <p>Tražim gosta…</p>
                </div>
                <GuestInfo v-else-if="result === SCAN_RESULT.FOUND" :guest="guest" @updated="guest = $event"></GuestInfo>
                <p v-else class="error-text">{{ resultMessage }}</p>
                <button type="button" class="closeBtn" @click="resultOpen = false">Zatvori</button>
            </v-card>
        </v-dialog>
    </div>
</template>

<script>
import { api } from "@/plugins/api";
import { StreamBarcodeReader } from "vue-barcode-reader";
import GuestInfo from "./GuestInfo.vue";
import { isBrucos, REQUEST_TIMEOUT } from '@/utils/guestTags';

const UUID_RE = /^[0-9A-F]{8}-[0-9A-F]{4}-[14][0-9A-F]{3}-[89AB][0-9A-F]{3}-[0-9A-F]{12}$/i;

const SCAN_RESULT = {
    FOUND: 'found',
    NOT_IN_DB: 'not-in-db',
    INVALID_QR: 'invalid-qr',
    ERROR: 'error',
};

const RESULT_MESSAGES = {
    [SCAN_RESULT.NOT_IN_DB]: 'QR kod i konfirmacijski kod su okej, ali kod nije u bazi podataka, pokušajte ponovno očitati kod, ili manualno unesite ime',
    [SCAN_RESULT.INVALID_QR]: 'QR kod je očitan, ali ne sadrži kod za potvrdu koji bi trebao sadržavati, pokušajte ponovno očitati kod, ili manualno unesite ime',
    [SCAN_RESULT.ERROR]: 'Greška prilikom dohvaćanja gosta, provjerite vezu i pokušajte ponovno',
};

export default {
    name: 'MobileEntry',
    components: {
        StreamBarcodeReader,
        GuestInfo
    },
    data() {
        return {
            SCAN_RESULT,
            guest: null,
            result: '',
            cameraOpen: false,
            resultOpen: false,
            lookingUp: false,
        }
    },
    computed: {
        resultMessage() {
            return RESULT_MESSAGES[this.result] || 'Dogodila se nepoznata greška, javite se administratoru';
        },
    },
    methods: {
        async onDecode(code) {
            if (this.lookingUp) return;
            this.cameraOpen = false;
            this.guest = null;

            if (!UUID_RE.test(code)) {
                this.showResult(SCAN_RESULT.INVALID_QR);
                return;
            }

            // open the dialog right away so staff see the lookup is running on slow wifi
            this.lookingUp = true;
            this.resultOpen = true;
            try {
                const params = new URLSearchParams({ search: code, search_fields: 'confCode' });
                const { data } = await api.get('/guests/', { params, timeout: REQUEST_TIMEOUT });
                // search is a contains-match, so require the exact code here
                const scanned = code.toLowerCase();
                this.guest = data.find(g => g.confCode?.toLowerCase() === scanned && isBrucos(g.tag)) || null;
                this.showResult(this.guest ? SCAN_RESULT.FOUND : SCAN_RESULT.NOT_IN_DB);
            } catch (err) {
                this.showResult(SCAN_RESULT.ERROR);
            } finally {
                this.lookingUp = false;
            }
        },
        showResult(result) {
            this.result = result;
            this.resultOpen = true;
        },
    }
}
</script>

<style scoped>
.qr-trigger {
    padding: 0;
    border: 0;
    background: none;
    cursor: pointer;
}

.qr-icon {
    height: 50px;
}

.lookup {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px;
}

.closeBtn {
    display: block;
    width: 93%;
    height: 30px;
    margin: -10px 10px 10px 10px;
    border: 1px solid black;
    border-radius: 10px;
    background-color: white;
    text-align: center;
}

.error-text {
    min-height: 80px;
    color: black;
    padding: 2%;
}
</style>
