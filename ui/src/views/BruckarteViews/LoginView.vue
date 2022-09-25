<template>
    <div id="login">
        <br>
        <div class="row justify-content-center">
            <div class="col-md-8">
                <div class="card">
                    <div class="card-header">Login</div>
                    <div class="card-body">
                        <div id="signin_button"></div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import VueJwtDecode from 'vue-jwt-decode'
import store from '@/store/index.js';
export default {
    components: {
    },
    el: '#app',
    computed: {
        privilege() {
            return store.state.privilege;
        },
        name() {
            return store.state.name;
        },
        id() {
            return store.state.id;
        },
        email() {
            return store.state.email;
        },
        tokenExp() {
            return store.state.tokenExp;
        }
    },
    data() {
        return {
            resp: '',
        }

    },
    methods: {

        handleCredentialResponse(res) {
            const responsePayload = VueJwtDecode.decode(res.credential);

            store.commit('setId', responsePayload.sub)
            store.commit('setName', decodeURIComponent(escape(responsePayload.name)));
            store.commit('setEmail', responsePayload.email)
            store.commit('setTokenExp', responsePayload.exp)



            axios.get(process.env.VUE_APP_BASE_URL + ':8000/users/',)
                .then(response => {
                    this.users = response.data;

                    var ids = [];
                    var nextId = -1;
                    var registeredEmail = false;


                    this.users.forEach(element => {
                        ids.push(element.id);

                        if (element.email == responsePayload.email) {
                            registeredEmail = true
                            store.commit('setPrivilege', element.privilege)
                            if (element.name == "") {
                                axios.put(process.env.VUE_APP_BASE_URL + ':8000/users/' + element.id + '/',
                                    { name: decodeURIComponent(escape(responsePayload.name)) },
                                    { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } }
                                )
                            }
                        }
                    });
                    for (let index = 0; index < ids.length; index++) {
                        if (ids.includes(String(index)) == false) {
                            nextId = index;
                            break;
                        }
                    }

                    if (nextId == -1) {
                        nextId = ids.length;
                    }

                    if (!registeredEmail) {
                        axios.post(process.env.VUE_APP_BASE_URL + ':8000/users/',
                            { id: nextId, name: decodeURIComponent(escape(responsePayload.name)), email: responsePayload.email, privilege: '0' },
                            { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } }
                        )
                        store.commit('setPrivilege', '0')
                    }
                    this.$router.push({ name: 'home' })
                })



        }


    },
    mounted: function () {
        if (!window.location.hash) {
            window.location = window.location + '#loaded';
            window.location.reload();
        }
        let googleScript = document.createElement('script');
        googleScript.src = 'https://accounts.google.com/gsi/client';
        document.head.appendChild(googleScript);

        window.addEventListener('load', () => {
            window.google.accounts.id.initialize({
                client_id: "729300808359-9qt44p6ksjivnbfd981pgjbmkh4ifgcj.apps.googleusercontent.com",
                /* RESTRIKCIJA DOMENE NA kset.org
                hosted_domain: "kset.org",*/
                callback: this.handleCredentialResponse,

            });
            window.google.accounts.id.renderButton(
                document.getElementById("signin_button"),
                { theme: "outline", size: "large" }  // customization attributes
            );
        })
    }

}
</script>

<style >
#signin_button {
    text-align: center;
    justify-content: center;
    align-items: center;
}
</style>