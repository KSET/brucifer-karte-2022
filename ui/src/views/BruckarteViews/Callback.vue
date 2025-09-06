<template>
    <div>Signing you in…</div>
</template>

<script>
import axios from 'axios'
import store from '@/store/index.js'

export default {
    async mounted() {
        const params = new URLSearchParams(window.location.search)
        const code = params.get('code')
        const returnedState = params.get('state')
        const storedState = sessionStorage.getItem('oauth_state')
        const verifier = sessionStorage.getItem('pkce_verifier')
        const redirectUri = process.env.VUE_APP_OAUTH_REDIRECT_URI || `${window.location.origin}/admin/callback`

        if (!code || !returnedState || !verifier || returnedState !== storedState) {
            this.$router.replace({ name: 'login' })
            return
        }

        try {
            const { data } = await axios.post(
                `${process.env.VUE_APP_BASE_URL}/auth/exchange/`,
                { code, code_verifier: verifier, redirect_uri: redirectUri },
                { withCredentials: true },
            )

            const me = await axios.get(`${process.env.VUE_APP_BASE_URL}/me/`, { withCredentials: true, headers: { Authorization: `Bearer ${data.access}` } })

            store.commit('setId', me.data.id)
            store.commit('setName', me.data.name)
            store.commit('setEmail', me.data.email)
            if (me.data.privilege !== undefined) store.commit('setPrivilege', me.data.privilege)

            switch (store.state.privilege) {
                case 2: this.$router.replace({ name: 'entry' }); break
                case 3: this.$router.replace({ name: 'guests' }); break
                default: this.$router.replace({ name: 'home' })
            }
        } catch (e) {
            this.$router.replace({ name: 'login' })
        } finally {
            sessionStorage.removeItem('pkce_verifier')
            sessionStorage.removeItem('oauth_state')
            sessionStorage.removeItem('oauth_nonce')
        }
    },
}
</script>
