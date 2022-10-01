<template>
    <div class="bw-page-container">
        <div class="lineup">
            <div v-for="user in users" :key="user.id">
                <div class="artist" title="{{ user.name }}">
                    <div class="image-container">
                        <div class="image-sizer2"></div>
                        <img class="image-frame2" v-bind:src="user.image">
                    </div>
                    <h3>{{ user.name }}</h3>
                </div>
            </div>
        </div>
        <Footer></Footer>
    </div>
</template>

<script>
import Footer from '@/components/NavbarAndFooter/Footer.vue'

import axios from 'axios'
export default {
    name: 'UsersTable',
    components: { Footer },
    props: {
        msg: String
    },
    data() {
        return {
            users: [],
            id: '',
            name: '',
            email: '',
            privilege: '',
        }

    },
    mounted() {
        this.created();
    },

    methods: {
        created() {
            axios.get(process.env.VUE_APP_BASE_URL + '/lineup/?ordering=order&search=1&search_fields=visible',)
                .then(response => {
                    this.users = response.data;
                    var ids = [];
                    this.users.forEach(element => {
                        ids.push(element.id);
                    });
                    if (ids.includes(String(314159)) == true) {
                        this.users.splice(this.users.length - 1, 1);

                    } else {
                        this.users = [];
                    }

                })
        },
        changeprivilege(user, changenum) {
            axios.put(process.env.VUE_APP_BASE_URL + '/users/' + user.id + '/',
                { privilege: changenum },
                { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } }
            )
                .then(() => {
                    this.created();
                })
        },
        deleteUser(user) {
            axios.delete(process.env.VUE_APP_BASE_URL + '/users/' + user.id + '/',
                { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } }
            )
                .then(() => {
                    this.created();
                })
        },
        searchUser() {
            axios.get(process.env.VUE_APP_BASE_URL + '/users/?search=' + this.search,)
                .then(response => {
                    this.users = response.data;
                })
        }
    }

}


</script>


<style>
@import "@fontsource/antonio";

.bw-page-container {
    margin-top: 0;
    flex: 1;

    position: relative;
    background-repeat: repeat;
    background-size: cover;
    background-color: linear-gradient(red, #F6BB96);
    min-height: 100vh;
    padding-bottom: 60px;
}

.lineup {
    padding: 3.14159em;

    padding-top: 5.5em;
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    grid-row-gap: 3.45rem;
    grid-column-gap: 5.25rem;
    will-change: grid-row-gap, grid-column-gap;
    transition-duration: .2s;
    transition-timing-function: ease;
    transition-property: grid-row-gap, grid-column-gap;
}

.image-container {
    position: relative;
}

.image-container .image-sizer2 {
    padding-bottom: calc(0.86 * 100%);
    transition: padding-bottom .3s ease;
    will-change: padding-bottom;
}

.image-container .image-frame2 {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-repeat: no-repeat;
    background-position: center center;
    background-size: contain;
}

.artist {
    background: rgba(0, 0, 0, .3);
    border-radius: 18px;
    padding: 15px 30px;
}

.artist h3 {
    text-align: center;
    font-style: normal;
    font-weight: normal;
    font-size: 2.25rem;
    color: white;
    text-transform: uppercase;
    margin-top: .3em;
    will-change: font-size;
    transition-duration: .2s;
    transition-timing-function: ease;
    transition-property: font-size;
}

@media screen and (max-width: 1550px) {
    .lineup {
        grid-template-columns: repeat(3, minmax(0, 1fr));
        grid-column-gap: 3rem;
    }

    .artist {
        padding: 15px 30px;
    }

    .artist h3 {
        font-size: 1.85rem;
    }
}

@media screen and (max-width: 980px) {
    .lineup {
        grid-template-columns: repeat(3, minmax(0, 1fr));
        grid-column-gap: 2.85rem;
    }

    .artist {
        padding: 10px 20px;
    }

    .artist h3 {
        font-size: 1.4rem;
    }
}

@media screen and (max-width: 635px) {
    .lineup {
        grid-template-columns: repeat(2, minmax(0, 1fr));
        grid-column-gap: 2rem;
    }

    .artist h3 {
        font-size: 1.1rem;
    }
}

@media screen and (max-width: 350px) {
    .lineup {
        grid-template-columns: repeat(1, minmax(0, 1fr));
        grid-row-gap: 1.2rem;
    }


    .artist {
        padding: 8px 12px;
    }
}
</style>


