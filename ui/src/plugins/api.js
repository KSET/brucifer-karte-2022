import axios from "axios";
import store from "@/store/index.js";

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

        if (
            error.response &&
            error.response.status === 401 &&
            !originalRequest._retry
        ) {
            originalRequest._retry = true;
            try {
                const refreshResponse = await axios.post(
                    `${process.env.VUE_APP_BASE_URL}/auth/token/refresh/`,
                    { refresh: store.state.refreshToken }
                );

                const newAccess = refreshResponse.data.access;
                store.commit("setAccessToken", newAccess);

                originalRequest.headers.Authorization = `Bearer ${newAccess}`;
                return api(originalRequest);
            } catch (refreshError) {
                store.commit("clearAuth");
                window.location = "/admin/login";
                return Promise.reject(refreshError);
            }
        }
        return Promise.reject(error);
    }
);

export default {
    install(app) {
        app.config.globalProperties.$api = api;
        app.provide("api", api);
    },
};
