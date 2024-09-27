<template>
    <div id="login" style="margin-top: 3.75rem; overflow: hidden;">
        <br>
        <div class="row justify-content-center">
            <div class="col-md-8">
                <div class="card" style="height: 100% !important">
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
        base64UrlDecode(str) {
            return decodeURIComponent(atob(str.replace(/-/g, '+').replace(/_/g, '/')));
        },
        handleCredentialResponse(res) {
            const tokenParts = res.credential.split('.'); // JWT format: header.payload.signature
            if (tokenParts.length === 3) {
                const payload = this.base64UrlDecode(tokenParts[1]);
                const responsePayload = JSON.parse(payload);

                // Proceed with your existing logic
                store.commit('setId', responsePayload.sub);
                store.commit('setName', decodeURIComponent(escape(responsePayload.name)));
                store.commit('setEmail', responsePayload.email);
                store.commit('setTokenExp', responsePayload.exp);
                // Fetch users from the server
                axios.get(`${process.env.VUE_APP_BASE_URL}/users/`).then(response => {
                    this.users = response.data;

                    let registeredEmail = this.users.some(user => {
                        if (user.email === responsePayload.email) {
                            // Update privilege and check for empty name to update
                            store.commit('setPrivilege', user.privilege);
                            if (!user.name) {
                                axios.put(`${process.env.VUE_APP_BASE_URL}/users/${user.id}/`, {
                                    name: decodeURIComponent(escape(responsePayload.name)),
                                }, {
                                    auth: {
                                        username: process.env.VUE_APP_DJANGO_USER,
                                        password: process.env.VUE_APP_DJANGO_PASS,
                                    }
                                });
                            }
                            return true; // Email is registered
                        }
                        return false; // Continue checking
                    });

                    // Register new user if email not found
                    if (!registeredEmail) {
                        axios.post(`${process.env.VUE_APP_BASE_URL}/users/`, {
                            name: decodeURIComponent(escape(responsePayload.name)),
                            email: responsePayload.email,
                            privilege: '0',
                        }, {
                            auth: {
                                username: process.env.VUE_APP_DJANGO_USER,
                                password: process.env.VUE_APP_DJANGO_PASS,
                            }
                        });
                        store.commit('setPrivilege', '0');
                    }

                    // Redirect based on privilege level
                    switch (this.privilege) {
                        case 2:
                            this.$router.push({ name: 'entry' });
                            break;
                        case 3:
                            this.$router.push({ name: 'guests' });
                            break;
                        default:
                            this.$router.push({ name: 'home' });
                    }
                });
            } else {
                console.error("Invalid JWT format");
            }
        }



    },
    mounted: function () {
        let googleScript = document.createElement('script');
        googleScript.src = 'https://accounts.google.com/gsi/client';
        document.head.appendChild(googleScript);

        window.addEventListener('load', () => {
            window.google.accounts.id.initialize({
                client_id: "729300808359-9qt44p6ksjivnbfd981pgjbmkh4ifgcj.apps.googleusercontent.com",
                hosted_domain: "kset.org",
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

<style>
#signin_button {
    text-align: center;
    justify-content: center;
    align-items: center;
}
</style>