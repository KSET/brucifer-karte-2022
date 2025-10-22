import axios from "axios";

export const publicApi = axios.create({
    baseURL: process.env.VUE_APP_BASE_URL,
});
