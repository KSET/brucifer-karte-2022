<template>
    <div id="visibility">
        <Sidebar />
        <div class="admin-page-container">
            <h1 class="page-title">Visibility</h1>

            <div class="visibility-grid">
                <h1 class="textfield">
                    Prikaz stranice Coming soon
                </h1>
                <button v-if="COMINGSOON_VISIBILITY == 1" class="button change"
                    @click="changeVisibility('COMINGSOON_VISIBILITY', '0')">
                    <img src="../../assets/icons/yes-icon.svg">
                </button>
                <button v-else class="button change" @click="changeVisibility('COMINGSOON_VISIBILITY', '1')"
                    style="background-color: white;">
                    <img class="image1" src="../../assets/icons/no-icon.svg">
                </button>

                <h1 class="textfield">
                    Prikaz stranice Izvođača
                </h1>
                <button v-if="LINEUP_VISIBILITY == 1" class="button change"
                    @click="changeVisibility('LINEUP_VISIBILITY', '0')">
                    <img src="../../assets/icons/yes-icon.svg">
                </button>
                <button v-else class="button change" @click="changeVisibility('LINEUP_VISIBILITY', '1')"
                    style="background-color: white;">
                    <img class="image1" src="../../assets/icons/no-icon.svg">
                </button>

                <h1 class="textfield">
                    Prikaz stranice Sponzora
                </h1>
                <button v-if="SPONSORS_VISIBILITY == 1" class="button change"
                    @click="changeVisibility('SPONSORS_VISIBILITY', '0')">
                    <img src="../../assets/icons/yes-icon.svg">
                </button>
                <button v-else class="button change" @click="changeVisibility('SPONSORS_VISIBILITY', '1')"
                    style="background-color: white;">
                    <img class="image1" src="../../assets/icons/no-icon.svg">
                </button>

                <h1 class="textfield">
                    Prikaz stranice Cjenik
                </h1>
                <button v-if="CJENIK_VISIBILITY == 1" class="button change"
                    @click="changeVisibility('CJENIK_VISIBILITY', '0')">
                    <img src="../../assets/icons/yes-icon.svg">
                </button>
                <button v-else class="button change" @click="changeVisibility('CJENIK_VISIBILITY', '1')"
                    style="background-color: white;">
                    <img class="image1" src="../../assets/icons/no-icon.svg">
                </button>

                <h1 class="textfield">
                    Prikaz stranice Tlocrt
                </h1>
                <button v-if="TLOCRT_VISIBILITY == 1" class="button change"
                    @click="changeVisibility('TLOCRT_VISIBILITY', '0')">
                    <img src="../../assets/icons/yes-icon.svg">
                </button>
                <button v-else class="button change" @click="changeVisibility('TLOCRT_VISIBILITY', '1')"
                    style="background-color: white;">
                    <img class="image1" src="../../assets/icons/no-icon.svg">
                </button>

                <h1 class="textfield">
                    Prikaz stranice Satnica
                </h1>
                <button v-if="SATNICA_VISIBILITY == 1" class="button change"
                    @click="changeVisibility('SATNICA_VISIBILITY', '0')">
                    <img src="../../assets/icons/yes-icon.svg">
                </button>
                <button v-else class="button change" @click="changeVisibility('SATNICA_VISIBILITY', '1')"
                    style="background-color: white;">
                    <img class="image1" src="../../assets/icons/no-icon.svg">
                </button>

                <h1 class="textfield">
                    Prikaz stranice Ulaznica
                </h1>
                <button v-if="ULAZNICA_VISIBILITY == 1" class="button change"
                    @click="changeVisibility('ULAZNICA_VISIBILITY', '0')">
                    <img src="../../assets/icons/yes-icon.svg">
                </button>
                <button v-else class="button change" @click="changeVisibility('ULAZNICA_VISIBILITY', '1')"
                    style="background-color: white;">
                    <img class="image1" src="../../assets/icons/no-icon.svg">
                </button>

                <h1 class="textfield">
                    Prikaz stranice Igrice
                </h1>
                <button v-if="IGRICA_VISIBILITY == 1" class="button change"
                    @click="changeVisibility('IGRICA_VISIBILITY', '0')">
                    <img src="../../assets/icons/yes-icon.svg">
                </button>
                <button v-else class="button change" @click="changeVisibility('IGRICA_VISIBILITY', '1')"
                    style="background-color: white;">
                    <img class="image1" src="../../assets/icons/no-icon.svg">
                </button>

                <h1 class="textfield">
                    Prikaz stranice Timera
                </h1>
                <button v-if="TIMER_VISIBILITY == 1" class="button change"
                    @click="changeVisibility('TIMER_VISIBILITY', '0')">
                    <img src="../../assets/icons/yes-icon.svg">
                </button>
                <button v-else class="button change" @click="changeVisibility('TIMER_VISIBILITY', '1')"
                    style="background-color: white;">
                    <img class="image1" src="../../assets/icons/no-icon.svg">
                </button>

                <h1 class="textfield">
                    Vrijeme odbrojavanja Timera
                </h1>
                <label class="datetimePicker">
                    <input @change="changeVisibility('TIMER_TIME', timerTime)" type="datetime-local" v-model="timerTime"
                        class="datetimePickerInput">
                    <span class="placeholderText">{{ formattedTimerTime }}</span>
                </label>

                <h1 class="textfield">
                    Vrijeme sponzorima za unos
                </h1>
                <label class="datetimePicker">
                    <input @change="changeVisibility('SPONSORS_INPUT_TIME', sponsorsInputTime)" type="datetime-local"
                        v-model="sponsorsInputTime" class="datetimePickerInput">
                    <span class="placeholderText">{{ formattedSponsorsInputTime }}</span>
                </label>

                <div>
                    <label for="startIndex">Start Index:</label>
                    <input v-model="startIndex" type="number" id="startIndex" placeholder="Enter start index" />

                    <label for="endIndex">End Index:</label>
                    <input v-model="endIndex" type="number" id="endIndex" placeholder="Enter end index" />

                    <button @click="sendEmailsInRange(startIndex, endIndex)">Send Emails</button>
                </div>
            </div>

        </div>
    </div>
</template>

<script>
import { api } from "@/plugins/api";
import Sidebar from '@/components/NavbarAndFooter/Sidebar.vue'
import store from "@/store/visibilityStore.js";
import { result } from 'lodash';

export default {
    name: 'VisibilityView',
    components: {
        Sidebar,
    },
    data() {
        return {
            timerTime: '',
            sponsorsInputTime: '',
            startIndex: 0,
            endIndex: 0,
            guests: [],
            sentGuestIds: new Set(), // Track sent guest IDs
        }
    },
    computed: {
        COMINGSOON_VISIBILITY() {
            return store.state.COMINGSOON_VISIBILITY;
        },
        LINEUP_VISIBILITY() {
            return store.state.LINEUP_VISIBILITY;
        },
        SPONSORS_VISIBILITY() {
            return store.state.SPONSORS_VISIBILITY;
        },
        CJENIK_VISIBILITY() {
            return store.state.CJENIK_VISIBILITY;
        },
        SATNICA_VISIBILITY() {
            return store.state.SATNICA_VISIBILITY;
        },
        TLOCRT_VISIBILITY() {
            return store.state.TLOCRT_VISIBILITY;
        },
        ULAZNICA_VISIBILITY() {
            return store.state.ULAZNICA_VISIBILITY;
        },
        TIMER_VISIBILITY() {
            return store.state.TIMER_VISIBILITY;
        },
        IGRICA_VISIBILITY() {
            return store.state.IGRICA_VISIBILITY;
        },
        formattedTimerTime() {
            const timerTime = store.state.TIMER_TIME;
            const formattedDate = timerTime.substring(8, 10) + '.' + timerTime.substring(5, 7) + '.' + timerTime.substring(0, 4);
            const formattedTime = timerTime.substring(11, 16);
            return formattedDate + '. ' + formattedTime;
        },
        formattedSponsorsInputTime() {
            const timerTime = store.state.SPONSORS_INPUT_TIME;
            const formattedDate = timerTime.substring(8, 10) + '.' + timerTime.substring(5, 7) + '.' + timerTime.substring(0, 4);
            const formattedTime = timerTime.substring(11, 16);
            return formattedDate + '. ' + formattedTime;
        },
    },
    methods: {
        async changeVisibility(changeField, val) {
            if (changeField == "TIMER_TIME" || changeField == "SPONSORS_INPUT_TIME") {
                if (window.confirm("Pokušavate promijeniti jedno od VREMENA, jeste li sigurni?")) {
                    await api.put(process.env.VUE_APP_BASE_URL + '/visibility/' + changeField + '/',
                        { visible: val },
                    )
                    await store.dispatch("fetchVisibilityData")
                }
            } else {
                await api.put(process.env.VUE_APP_BASE_URL + '/visibility/' + changeField + '/',
                    { visible: val },
                )
                await store.dispatch("fetchVisibilityData")
            }

        },
        async sendEmailsInRange(start, end) {
            try {
                // Fetch all guests who bought a ticket
                let res = await api.get(`${process.env.VUE_APP_BASE_URL}/guests/?search=1&search_fields=bought`);
                this.guests = res.data;

                // Initialize counter
                let sentCount = 0;
                const totalToSend = end - start + 1;

                // Loop through the specified range
                for (let i = start; i <= end && i < this.guests.length; i++) {
                    const guest = this.guests[i];

                    // Check if the guest has already been sent an email in this session
                    if (!this.sentGuestIds.has(guest.id)) {
                        await this.sendMail(guest);
                        this.sentGuestIds.add(guest.id); // Mark guest as sent
                        sentCount++; // Increment counter

                        // Display progress in the console
                        console.log(`Email sent to ${guest.jmbag} (${sentCount}/${totalToSend})`);
                    }
                }

                console.log("Emails sent successfully within the specified range.");
            } catch (error) {
                console.error("Error sending emails:", error);
            }
        },

        async sendMail(guest) {
            console.log("Sending email...");


            var jmbagslice = guest.jmbag;
            if (jmbagslice.slice(0, 3) == "003") {
                jmbagslice = jmbagslice.slice(4, 9);
            } else if (jmbagslice.slice(0, 1) == "0") {
                jmbagslice = jmbagslice.slice(0, 9);
            } else {
                jmbagslice = jmbagslice.slice(2, 7);
            }

            var e_name = guest.name[0].toLowerCase()
            if (e_name == "č") {
                e_name = "c";
            } else if (e_name == "š") {
                e_name = "s";
            } else if (e_name == "ž") {
                e_name = "z";
            } else if (e_name == "đ") {
                e_name = "d";
            } else if (e_name == "ć") {
                e_name = "c";
            }

            var e_surname = guest.surname[0].toLowerCase()
            if (e_surname == "č") {
                e_surname = "c";
            } else if (e_surname == "š") {
                e_surname = "s";
            } else if (e_surname == "ž") {
                e_surname = "z";
            } else if (e_surname == "đ") {
                e_surname = "d";
            } else if (e_surname == "ć") {
                e_surname = "c";
            }


            var email = e_name + e_surname + jmbagslice + "@fer.hr";

            // za testiranje, maknuti u produkciji
            // email = "pavleergovic@gmail.com"

            var msg = guest.name + " " + guest.surname + " " + guest.confCode

            try {
                // Send email
                await api.post(
                    `${process.env.VUE_APP_BASE_URL}/mailer/send_mail/`,
                    {
                        emails: [
                            {
                                subject: "[#BRUCIFER25] Potvrda za kupljenu kartu",
                                template: "guest_email",
                                message: msg,
                                name: guest.name,
                                confCode: guest.confCode,
                                to_mail: email,
                            },
                        ],
                    },
                    {
                        auth: {
                            username: process.env.VUE_APP_DJANGO_USER,
                            password: process.env.VUE_APP_DJANGO_PASS,
                        },
                    }
                );

                console.log(`Email sent to ${email}`);
            } catch (error) {
                console.error(`Failed to send email to ${email}`, error);
            }
        },

        sendEmails() {
            const start = parseInt(this.startIndex, 10);
            const end = parseInt(this.endIndex, 10);

            if (!isNaN(start) && !isNaN(end) && start <= end) {
                this.sendEmailsInRange(start, end);
            } else {
                alert("Please enter valid start and end indices.");
            }
        },


    }
}
</script>


<style>
.visibility-grid {
    display: grid;
    grid-template-columns: 70% 30%;
    row-gap: 10px;
    align-items: center;
    width: 50%;
}

.datetimePicker {
    border: 1px solid black;
    font-size: 15px;
    position: relative;
}

@media screen and (max-width: 980px) {
    .visibility-grid {
        width: 80%;
    }
}

@media screen and (max-width: 550px) {
    .visibility-grid {
        width: 90%;
    }

    .placeholderText {
        font-size: 12px;
    }

    .datetimePicker {
        width: 140%;
    }
}

.datetimePickerInput {
    width: 20px;
}

.placeholderText {
    position: absolute;
    top: 50%;
    left: 25px;
    transform: translateY(-50%);
}
</style>