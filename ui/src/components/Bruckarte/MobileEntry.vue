<template>
    <div>
        <button type="button" class="qr-trigger" aria-label="Skeniraj QR kod" @click="cameraOpen = true">
            <img class="qr-icon" src="../../assets/icons/qr-code-icon.svg" alt="">
        </button>

        <v-dialog v-model="cameraOpen" max-width="600">
            <v-card>
                <v-card-item>
                    <p v-if="cameraError" class="error-text">{{ cameraError }}</p>
                    <!-- v-if so the camera is released as soon as the dialog closes -->
                    <div v-else-if="cameraOpen" class="scanner">
                        <QrcodeStream :track="onTrack" @error="onCameraError"
                            @camera-on="cameraReady = true" @camera-off="cameraReady = false"></QrcodeStream>
                        <v-progress-circular v-if="!cameraReady" class="camera-loading" indeterminate color="primary"></v-progress-circular>
                    </div>
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
import { QrcodeStream, setZXingModuleOverrides } from "vue-qrcode-reader";
import zxingWasmUrl from "zxing-wasm/reader/zxing_reader.wasm";
import GuestInfo from "./GuestInfo.vue";
import { isBrucos, REQUEST_TIMEOUT } from '@/utils/guestTags';

setZXingModuleOverrides({
    locateFile: (path, prefix) => path.endsWith('.wasm') ? zxingWasmUrl : prefix + path,
});

const RESCAN_COOLDOWN = 1000;

const UUID_RE =/^[0-9A-F]{8}-[0-9A-F]{4}-[14][0-9A-F]{3}-[89AB][0-9A-F]{3}-[0-9A-F]{12}$/i;

const CAMERA_ERRORS = {
    NotAllowedError: 'Pristup kameri je odbijen, dopustite pristup kameri u postavkama preglednika',
    NotFoundError: 'Kamera nije pronađena na ovom uređaju',
    NotReadableError: 'Kamera je zauzeta, zatvorite druge aplikacije koje koriste kameru i pokušajte ponovno',
    OverconstrainedError: 'Stražnja kamera nije dostupna na ovom uređaju',
    InsecureContextError: 'Kamera radi samo preko HTTPS veze',
    StreamApiNotSupportedError: 'Ovaj preglednik ne podržava kameru, pokušajte s drugim preglednikom',
    NotSupportedError: 'Ovaj preglednik ne podržava kameru, pokušajte s drugim preglednikom',
    StreamLoadTimeoutError: 'Kamera se nije pokrenula na vrijeme, zatvorite i ponovno otvorite kameru',
};

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
        QrcodeStream,
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
            cameraReady: false,
            cameraError: '',
            lastCode: '',
            resultClosedAt: 0,
        }
    },
    computed: {
        resultMessage() {
            return RESULT_MESSAGES[this.result] || 'Dogodila se nepoznata greška, javite se administratoru';
        },
    },
    watch: {
        cameraOpen(open) {
            if (!open) {
                this.cameraReady = false;
                this.cameraError = '';
            }
        },
        resultOpen(open) {
            if (!open) this.resultClosedAt = Date.now();
        },
    },
    methods: {
        onTrack(codes) {
            const code = codes[0]?.rawValue;
            if (!code || this.lookingUp || this.resultOpen) return;
            if (code === this.lastCode && Date.now() - this.resultClosedAt < RESCAN_COOLDOWN) return;
            this.lastCode = code;
            navigator.vibrate?.(100);
            this.onDecode(code);
        },
        onCameraError(err) {
            this.cameraError = CAMERA_ERRORS[err.name] || `Greška s kamerom (${err.name || err.message}), javite se administratoru`;
        },
        async onDecode(code) {
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

.scanner {
    position: relative;
    min-height: 200px;
}

.camera-loading {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
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
