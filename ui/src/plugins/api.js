import axios from "axios";
import store from "@/store/index.js";
import { NONE } from "@/plugins/roles.js";

const NO_PRIVILEGE_MSG =
    "Nažalost, nemate privilegije za pristup ovoj stranici. Pričekajte ili se javite savjetniku";

// the router guard and the 403 handler can both deny the same event, so the
// alert is shown once and suppressed until the redirect navigation lands
let privilegeAlertShown = false;

export function alertNoPrivilege() {
    if (privilegeAlertShown) return;
    privilegeAlertShown = true;
    window.alert(NO_PRIVILEGE_MSG);
}

export function resetNoPrivilegeAlert() {
    privilegeAlertShown = false;
}

export const api = axios.create({
    baseURL: process.env.VUE_APP_BASE_URL,
});

api.interceptors.request.use((config) => {
    const token = store.state.accessToken;
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

api.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;

        if (error.response?.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;
            try {
                const refreshResponse = await api.post("/auth/token/refresh/", {
                    refresh: store.state.refreshToken,
                });

                const newAccess = refreshResponse.data.access;
                store.commit("setAccessToken", newAccess);

                // refresh tokens rotate — persist the new one each time
                if (refreshResponse.data.refresh) {
                    store.commit("setRefreshToken", refreshResponse.data.refresh);
                }

                originalRequest.headers.Authorization = `Bearer ${newAccess}`;
                return api(originalRequest);
            } catch (refreshError) {
                store.commit("clearAuth");
                window.location.href = "/admin/login";
                return Promise.reject(refreshError);
            }
        }

        if (error.response?.status === 403 && store.state.id !== "") {
            try {
                const role = await refreshRole();
                const { default: router } = await import("@/router/index.js");
                const allowed = router.currentRoute.value.meta.roles;
                if (role === NONE) {
                    alertNoPrivilege();
                    store.commit("clearAuth");
                    window.location.href = "/admin/login";
                } else if (allowed !== undefined && !allowed.includes(role)) {
                    alertNoPrivilege();
                    router.replace({ path: "/admin" });
                }
            } catch (e) {
            }
        }
        return Promise.reject(error);
    }
);

let roleFetch = null;

export function refreshRole() {
    if (roleFetch === null) {
        roleFetch = api
            .get("/me/")
            .then(({ data }) => {
                store.commit("setRole", data.role);
                return data.role;
            })
            .finally(() => {
                roleFetch = null;
            });
    }
    return roleFetch;
}

export default {
    install(app) {
        app.config.globalProperties.$api = api;
        app.provide("api", api);
    },
};
