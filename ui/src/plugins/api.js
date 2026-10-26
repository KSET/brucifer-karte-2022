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

const clientConfig = {
    baseURL: process.env.VUE_APP_BASE_URL,
    withCredentials: true,
};

export const api = axios.create(clientConfig);

const authClient = axios.create({
    ...clientConfig,
    headers: { "X-Requested-With": "XMLHttpRequest" },
});

const isSessionRejected = (error) => error.response?.status === 401;
const isTransient = (error) => !error.response || error.response.status >= 500;
const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

async function postRefresh(attempt = 0) {
    try {
        return await authClient.post("/auth/token/refresh/");
    } catch (error) {
        const retry = isTransient(error)
            ? attempt < 2
            : !navigator.locks && isSessionRejected(error) && attempt === 0;
        if (!retry) throw error;
        await sleep(1000 * 2 ** attempt);
        return postRefresh(attempt + 1);
    }
}

let tokenRefresh = null;

export function refreshAccessToken() {
    if (tokenRefresh === null) {
        const doRefresh = () =>
            postRefresh().then(({ data }) => {
                store.commit("setAccessToken", data.access);
                store.commit("setUser", data.user);
                return data.access;
            });
        tokenRefresh = (navigator.locks
            ? navigator.locks.request("brucifer-token-refresh", doRefresh)
            : doRefresh()
        ).finally(() => {
            tokenRefresh = null;
        });
    }
    return tokenRefresh;
}

// Resolves to true when it just refreshed (and so already loaded the user).
export async function restoreSession() {
    if (store.state.accessToken) return false;
    try {
        await refreshAccessToken();
        return true;
    } catch (error) {
        if (isSessionRejected(error)) {
            store.commit("clearAuth");
        } else {
            console.error("Session restore failed:", error);
        }
        return false;
    }
}

let pendingAuthGuards = 0;

export async function whileAuthGuardPending(fn) {
    pendingAuthGuards++;
    try {
        return await fn();
    } finally {
        pendingAuthGuards--;
    }
}

export async function login(googleCredential) {
    const { data } = await authClient.post("/auth/google/", {
        token: googleCredential,
    });
    store.commit("setAccessToken", data.access);
    store.commit("setUser", data.user);
    return data.user;
}

export async function logout() {
    try {
        await authClient.post("/auth/logout/");
    } catch (e) {
    }
    store.commit("clearAuth");
}

async function redirectToLogin() {
    store.commit("clearAuth");
    if (pendingAuthGuards > 0) return;
    const { default: router } = await import("@/router/index.js");
    const current = router.currentRoute.value;
    if (current.name !== "login") {
        router.replace({ name: "login", query: { redirect: current.fullPath } });
    }
}

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

        if (error.response?.status === 401 && !originalRequest._retry && store.state.accessToken) {
            originalRequest._retry = true;
            try {
                if (originalRequest.headers.Authorization === `Bearer ${store.state.accessToken}`) {
                    await refreshAccessToken();
                }
                return api(originalRequest);
            } catch (refreshError) {
                if (isSessionRejected(refreshError)) {
                    await redirectToLogin();
                }
                return Promise.reject(refreshError);
            }
        }

        if (error.response?.status === 403 && store.getters.isLoggedIn) {
            try {
                const role = await refreshRole();
                const { default: router } = await import("@/router/index.js");
                const allowed = router.currentRoute.value.meta.roles;
                if (role === NONE) {
                    alertNoPrivilege();
                    await logout();
                    router.replace({ name: "login" });
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
                store.commit("setUser", data);
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
