<template>
    <div id="firme">
        <Sidebar />
        <div class="admin-page-container">
            <h1 class="page-title">AAAAAAAAAAAAAAAAA TESTTTTTTTT GITTTTT</h1>
            <h1 class="page-title">Firme</h1>

            <h1 class="textfield">Ime Firme</h1>
            <input @input="searchFirm" class="inputfield" type="text" v-model="search">
            <table class="table" id="guests">
                <thead>
                    <th>Firma</th>
                    <th>Odobreno</th>
                    <th>Upisano</th>
                    <th>Ušlo</th>
                </thead>
                <tbody>
                    <tr v-for="guest in firms" :key="guest.id">
                        <td>{{ guest.name }}</td>
                        <td>{{ guest.guestCap }}</td>
                        <td>{{ guest.guestsAdded }}</td>
                        <td>{{ guest.guetsEntered }}</td>
                    </tr>
                </tbody>
            </table>

        </div>
    </div>

</template>
  
<script>
import axios from 'axios'
import Sidebar from '@/components/NavbarAndFooter/Sidebar.vue'

export default {
    name: 'GuestsTable',
    props: {
        msg: String
    },
    components: {
        Sidebar
    },
    data() {
        return {
            firms: [],
            search: '',

            guestsAdded: '',
            guetsEntered: 0,
        }
    },
    mounted() {
        this.created();
    },
    methods: {
        created() {
            axios.get(process.env.VUE_APP_BASE_URL + '/sponsors/',)
                .then(response => {
                    this.firms = response.data;
                    this.firms.splice(0, 1);

                    this.firms.forEach(element => {
                        axios.get(process.env.VUE_APP_BASE_URL + '/guests/?search=' + element.slug + "&search_fields=tag")
                            .then(response => {
                                var sponsorGuests = response.data;
                                element.guestsAdded = sponsorGuests.length;
                                var enter = 0;
                                sponsorGuests.forEach(elementy => {
                                    if (elementy.entered == 1)
                                        enter = enter + 1;
                                });

                                element.guetsEntered = enter;
                            })

                    });

                })
        },
        searchFirm() {
            axios.get(process.env.VUE_APP_BASE_URL + '/sponsors/?search=' + this.search + "&search_fields=name",)
                .then(response => {
                    this.firms = response.data;
                    var ids = [];
                    this.firms.forEach(element => {
                        ids.push(element.id)
                    });
                    if (ids.includes('314159')) {
                        this.firms.splice(0, 1);
                    }

                    this.firms.forEach(element => {
                        axios.get(process.env.VUE_APP_BASE_URL + '/guests/?search=' + element.slug + "&search_fields=tag")
                            .then(response => {
                                var sponsorGuests = response.data;
                                element.guestsAdded = sponsorGuests.length;
                                var enter = 0;
                                sponsorGuests.forEach(elementy => {
                                    if (elementy.entered == 1)
                                        enter = enter + 1;
                                });

                                element.guetsEntered = enter;
                            })

                    });
                })
        }
    }

}
</script>

  
  
  