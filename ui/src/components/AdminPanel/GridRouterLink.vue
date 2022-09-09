<template>
    <div class="sidenav">
        <RouterElement class="sidebar-element"   :name="'Tagovi'" :link="'/bruckarte/tags'"></RouterElement>
        <RouterElement class="sidebar-element"  :name="'Privilegije'" :link="'/bruckarte/privileges'"></RouterElement>
        <RouterElement class="sidebar-element"  :name="'Korisnici'" :link="'/bruckarte/users'"></RouterElement>
        <RouterElement class="sidebar-element"  :name="'Uvoz'" :link="'/bruckarte/import'"></RouterElement>
        <RouterElement class="sidebar-element"  :name="'Izvoz'" :link="'/bruckarte/export'"></RouterElement>
        <button class="dropdown-btn" >Izvođači 
            <img class="dropdown-icon" src="@/assets/icons/dopdwn-notopen-icon.svg" @click="toggleDropdown">
        </button>
        <div class="dropdown-container">
            <RouterElement class="sidebar-element"  :name="'Pregled Izvođača'" :link="'/bruckarte/lineup'"></RouterElement>
            <RouterElement class="sidebar-element"  :name="'Dodavanje Izvođača'" :link="'/bruckarte/lineup-add/0'"></RouterElement>
        </div>
        <button class="dropdown-btn" @click="toggleDropdown">Sponzori
            <img class="dropdown-icon" src="@/assets/icons/dopdwn-notopen-icon.svg" @click="toggleDropdown">
        </button>
        <div class="dropdown-container">
            <RouterElement class="sidebar-element"  :name="'Pregled Sponzora'" :link="'/bruckarte/sponsors'"></RouterElement>
            <RouterElement class="sidebar-element"  :name="'Dodavanje Sponzora'" :link="'/bruckarte/sponsors-add/0'"></RouterElement>

        </div>
        <RouterElement class="sidebar-element"  :name="'Dodaj Gosta'" :link="'/bruckarte/guests-add'"></RouterElement>
        <RouterElement class="sidebar-element"  :name="'Kontakt'" :link="'/bruckarte/sponsors'"></RouterElement>
    </div>
</template>

<script>
import RouterElement from './RouterElement.vue';

export default {
    name: "GridRouterLink",
    components: { RouterElement },
    data() {
        return {
            linkNames: ['Tags', 'Privileges', 'Users'],
            linkURLs: ['/tags', '/privileges', '/users']
        }
    },
    methods: {
        toggleDropdown() {
            var dropdown = document.getElementsByClassName("dropdown-btn");
            var i;

            for (i = 0; i < dropdown.length; i++) {
                dropdown[i].addEventListener("click", function () {
                    this.classList.toggle("active");
                    var dropdownContent = this.nextElementSibling;
                    if (dropdownContent.style.display === "block") {
                        dropdownContent.style.display = "none";
                    } else {
                        dropdownContent.style.display = "block";
                    }
                });
            }
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
    padding-top: 20px;
}

/* Style the sidenav links and the dropdown button */
.sidebar-element{
    padding: 6px 8px 6px 16px;
    text-decoration: none;
    font-size: 20px;
    display: block;
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
.dropdown-icon {
    float: right;
    padding-right: 2%;
    padding-top: 2%;
}
</style>
