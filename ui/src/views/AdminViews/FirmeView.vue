<template>
    <div id="firme">
        <Sidebar />
        <div class="admin-page-container">
            <h1 class="page-title">Firme</h1>

            <h1 class="textfield">Ime Firme</h1>
            <input @input="searchFirm" class="inputfield" type="text" v-model="name">
            <table class="table" id="guests">
                <thead>
                    <th>Firma</th>
                    <th>Odobreno</th>
                    <th>Upisano</th>
                    <th>Ušlo</th>
                </thead>
                <tbody>
                    <tr v-for="guest in firms" :key="guest.id">
                        <td>{{guest.name}}</td>
                        <td>{{guest.guestCap}}</td>
                        <td>{{guest.name}}</td>
                        <td>{{guest.guestCap}}</td>
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

                })
        },
        searchFirm() {
            axios.get(process.env.VUE_APP_BASE_URL + '/sponsors/?search=' + this.search + "&search_fields=name",)
                .then(response => {
                    this.firms = response.data;
                })
        }
    }

}
</script>

  
  
  