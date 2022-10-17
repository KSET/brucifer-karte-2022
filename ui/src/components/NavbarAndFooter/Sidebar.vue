<template>
    <div class="sidenav">
        <RouterElement class="sidebar-element" :name="'Tagovi'" :link="'/admin/tags'"></RouterElement>
        <RouterElement class="sidebar-element" :name="'Privilegije'" :link="'/admin/privileges'"></RouterElement>
        <RouterElement class="sidebar-element" :name="'Korisnici'" :link="'/admin/users'"></RouterElement>
        <RouterElement class="sidebar-element" :name="'Uvoz'" :link="'/admin/import'"></RouterElement>
        <button class="sidebar-element" @click="ExportData">
            Izvoz
        </button>

        <div class="sidbar-element" style="border-bottom: 1px solid black;" @click="toggleDropdownLineup"
            v-bind:style="[(showDropdownLineup) ? {backgroundColor:'#D9D9D9'}: { backgroundColor:'white'}]">
            <RouterElement class="sidebar-element" style="display: inline-block; width: 90%; border-bottom: none;"
                :name="'Izvođači'">
            </RouterElement>
            <img v-if="this.showDropdownLineup==false" class="dropdown-icon" style="z-index:-1"
                src="@/assets/icons/dopdwn-notopen-icon.svg" >
            <img style="z-index:-1" v-else class="dropdown-icon" src="@/assets/icons/dopdwn-open-icon.svg">

        </div>
        <RouterElement style="padding-left:3rem !important;" id="dpL1" class="sidebar-element"
            :name="'Pregled Izvođača'" :link="'/admin/lineup-list'">
        </RouterElement>
  
        <a style="padding-left:3rem !important; color: black;" id="dpL2" class="sidebar-element" href="/admin/lineup-add/0">Dodavanje Izvođača</a>


        <div class="sidbar-element" style="border-bottom: 1px solid black;" @click="toggleDropdownSponsors"
            v-bind:style="[(showDropdownSponsors) ? {backgroundColor:'#D9D9D9'}: { backgroundColor:'white'}]">
            <RouterElement class="sidebar-element" style="display: inline-block; width: 90%; border-bottom: none;"
                :name="'Sponzori'">
            </RouterElement>
            <img v-if="this.showDropdownSponsors==false" class="dropdown-icon"
                src="@/assets/icons/dopdwn-notopen-icon.svg" >
            <img v-else class="dropdown-icon" src="@/assets/icons/dopdwn-open-icon.svg">

        </div>
        <RouterElement style="padding-left:3rem !important;" id="dpS1" class="sidebar-element"
            :name="'Pregled Sponzora'" :link="'/admin/sponsors-list'">
        </RouterElement>
    
        <a style="padding-left:3rem !important; color: black;" id="dpS2" class="sidebar-element" href="/admin/sponsors-add/0">Dodavanje Sponzora</a>

        <RouterElement class="sidebar-element" :name="'Dodaj Gosta'" :link="'/admin/guests-add'"></RouterElement>
        <RouterElement class="sidebar-element" :name="'Kontakt'" :link="'/admin/band-kontakt'"></RouterElement>
        <RouterElement class="sidebar-element" :name="'Firme'" :link="'/admin/firme'"></RouterElement>
        <RouterElement class="sidebar-element" :name="'Cjenik'" :link="'/admin/cjenik'"></RouterElement>

    </div>
</template>

<script>
import axios from 'axios'
import RouterElement from '@/components/AdminPanel/RouterElement.vue'
import * as XLSX from 'xlsx'
export default {
    name: "GridRouterLink",
    components: { RouterElement },
    data() {
        return {
            showDropdownLineup: false,
            showDropdownSponsors: false,

            linkNames: ['Tags', 'Privileges', 'Users'],
            linkURLs: ['/tags', '/privileges', '/users'],
            users: [],
        }
    },
    mounted() {
        document.getElementById("dpL1").style.display = "none";
        document.getElementById("dpL2").style.display = "none";
        document.getElementById("dpS1").style.display = "none";
        document.getElementById("dpS2").style.display = "none";
    },
    methods: {
        toggleDropdownLineup() {
            this.showDropdownLineup = !this.showDropdownLineup;
            if (this.showDropdownLineup) {
                document.getElementById("dpL1").style.display = "block";
                document.getElementById("dpL2").style.display = "block";
            } else {
                document.getElementById("dpL1").style.display = "none";
                document.getElementById("dpL2").style.display = "none";
            }
        },
        toggleDropdownSponsors() {
            this.showDropdownSponsors = !this.showDropdownSponsors;
            if (this.showDropdownSponsors) {
                document.getElementById("dpS1").style.display = "block";
                document.getElementById("dpS2").style.display = "block";
            } else {
                document.getElementById("dpS1").style.display = "none";
                document.getElementById("dpS2").style.display = "none";
            }
        },
        ExportData() {
            var filename = 'export_guests.xlsx';
            axios.get(process.env.VUE_APP_BASE_URL + '/guests/',)
                .then(response => {
                    var data = response.data;
                    var ws = XLSX.utils.json_to_sheet(data);
                    var wb = XLSX.utils.book_new();
                    XLSX.utils.book_append_sheet(wb, ws, "People");
                    XLSX.writeFile(wb, filename);
                });


        }
    }
}
</script>

<style lang="scss" >
.sidenav {
    border-right: 1px solid #000000;
    margin-top: 3.75rem;
    width: 25%;
    height: 100%;
    position: fixed;
    z-index: 1;
    top: 0;
    left: 0;
    background-color: white;
    overflow-x: hidden;
}

/* Style the sidenav links and the dropdown button */
.sidebar-element {
    padding-left: 1.7rem !important;
    padding: 2.73% 8px 6px 16px;
    text-decoration: none;
    font-size: 20px;
    display: block;
    border: none;
    background: none;
    width: 100%;
    text-align: left !important;
    cursor: pointer;
    outline: none;
    display: block;
    height: 50px;
    text-align: left;
    font-family: 'Montserrat';
    font-style: normal;
    font-weight: 700;
    font-size: 16px;
    line-height: 36px;
    border-bottom: black;
    border-bottom: 1px solid #000000;
}

.dropdown-btn {
    padding: 6px 8px 6px 16px;
    text-decoration: none;
    font-size: 20px;
    border: none;
    background: none;
    width: 100%;
    text-align: left;
    cursor: pointer;
    outline: none;
    display: block;
    height: 50px;
    text-align: left;
    font-family: 'Montserrat';
    font-style: normal;
    font-weight: 700;
    font-size: 16px;
    line-height: 36px;
    border-bottom: black;
    border-bottom: 1px solid #000000;
}

/* On mouse-over */
.sidenav a:hover,
.dropdown-btn:hover {
    color: darkgray;
}

/* Main content */

/* Add an active class to the active dropdown button */
.active {
    background-color: gray;
    color: white;
}

/* Dropdown container (hidden by default). Optional: add a lighter background color and some left padding to change the design of the dropdown content */
.dropdown-container {
    display: none;
    background-color: white;
    padding-left: 8px;
}

/* Optional: Style the caret down icon */

.admin-page-container {
    position: relative;
    margin-top: 3.75rem;

    margin-left: 26%;
    /* Same as the width of the sidenav */
    margin-right: 1%;
    font-size: 28px;
    /* Increased text to enable scrolling */
    padding: 10px 10px;
    height: 91vh;
    overflow: hidden;
}

@media screen and (max-width: 900px) {
    .sidenav {
        display: none;
    }

    .admin-page-container {
        position: relative;

        margin-left: 1%;
    }
}
</style>
