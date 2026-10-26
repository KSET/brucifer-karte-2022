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
import { login, logout, alertNoPrivilege, resetNoPrivilegeAlert } from "@/plugins/api";
import { ADMIN, ENTRY, TICKETS, ENTRY_TICKETS } from "@/plugins/roles";

const HOME_BY_ROLE = {
    [TICKETS]: { name: "guests" },
    [ENTRY_TICKETS]: { name: "guests" },
    [ENTRY]: { name: "entry" },
    [ADMIN]: { name: "home" },
};

export default {
    name: "Login",
    methods: {
        async handleCredentialResponse(res) {
            const denyLogin = () => {
                alertNoPrivilege();
                resetNoPrivilegeAlert();
            };
            let user;
            try {
                user = await login(res.credential);
            } catch (err) {
                if (err.response?.data?.code === "no_privileges") {
                    denyLogin();
                } else {
                    console.error("Login failed:", err);
                }
                return;
            }

            if (!HOME_BY_ROLE[user.role]) {
                await logout();
                denyLogin();
                return;
            }
            const redirect = this.$route.query.redirect;
            this.$router.push(
                typeof redirect === "string" && redirect.startsWith("/admin")
                    ? redirect
                    : HOME_BY_ROLE[user.role]
            );
        },
    },
    mounted() {
        const init = () => {
            try {
                window.google.accounts.id.initialize({
                    client_id: process.env.VUE_APP_GOOGLE_CLIENT_ID,
                    hosted_domain: "kset.org",
                    callback: this.handleCredentialResponse,
                });
                window.google.accounts.id.renderButton(
                    document.getElementById("signin_button"),
                    { theme: "outline", size: "large" }
                );
            } catch (err) {
                console.error("Google Sign-In init failed:", err);
            }
        };

        if (window.google?.accounts?.id) {
            init();
            return;
        }

        const src = "https://accounts.google.com/gsi/client";
        let script = document.querySelector(`script[src="${src}"]`);
        if (!script) {
            script = document.createElement("script");
            script.src = src;
            script.async = true;
            script.defer = true;
            document.head.appendChild(script);
        }
        script.addEventListener("load", init);
        script.addEventListener("error", () =>
            console.error("Failed to load Google Sign-In script")
        );
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
