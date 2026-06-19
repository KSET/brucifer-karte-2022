<template>
    <div id="login" style="margin-top: 3.75rem; overflow: hidden;">
        <br />
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
import store from "@/store/index.js";
import { api } from "@/plugins/api";
import { NONE, ADMIN, ENTRY, TICKETS, ENTRY_TICKETS } from "@/plugins/roles";

export default {
    name: "Login",
    methods: {
        async handleCredentialResponse(res) {
            try {
                const response = await api.post("/auth/google/", {
                    token: res.credential,
                });

                const { access, refresh, user } = response.data;

                store.commit("setAccessToken", access);
                store.commit("setRefreshToken", refresh);
                store.commit("setId", user.id);
                store.commit("setName", user.name);
                store.commit("setEmail", user.email);
                store.commit("setPrivilege", user.privilege);
                store.commit("setRole", user.privilege);

                switch (user.privilege) {
                    case TICKETS:
                    case ENTRY_TICKETS:
                        this.$router.push({ name: "guests" });
                        break;
                    case ENTRY:
                        this.$router.push({ name: "entry" });
                        break;
                    case ADMIN:
                        this.$router.push({ name: "home" });
                        break;
                    case NONE:
                    default:
                        window.alert(
                            "Nažalost, nemate privilegije za pristup ovoj stranici. Pričekajte ili se javite savjetniku"
                        );
                        break;
                }
            } catch (err) {
                console.error("Login failed:", err);
            }
        },
    },
    mounted() {
        const googleScript = document.createElement("script");
        googleScript.src = "https://accounts.google.com/gsi/client";
        document.head.appendChild(googleScript);

        window.addEventListener("load", () => {
            window.google.accounts.id.initialize({
                client_id: process.env.VUE_APP_GOOGLE_CLIENT_ID,
                hosted_domain: "kset.org",
                callback: this.handleCredentialResponse,
            });
            window.google.accounts.id.renderButton(
                document.getElementById("signin_button"),
                { theme: "outline", size: "large" }
            );
        });
    },
};
</script>


<style>
#signin_button {
    text-align: center;
    justify-content: center;
    align-items: center;
}
</style>
