import axios from 'axios'

export const api = axios.create({
    baseURL: process.env.VUE_APP_BASE_URL,
    auth: {
        username: process.env.VUE_APP_DJANGO_USER,
        password: process.env.VUE_APP_DJANGO_PASS,
    },
})

export default {
    install(app) {
        app.config.globalProperties.$api = api
        app.provide('api', api)
    },
}
