<template>
    <div id="login" style="margin-top: 3.75rem; overflow: hidden;">
        <br />
        <div class="row justify-content-center">
            <div class="col-md-8">
                <div class="card" style="height: 100% !important">
                    <div class="card-header">Login</div>
                    <div class="card-body">
                        <div id="signin_button">
                            <button class="btn btn-outline-dark" @click="loginWithGoogle">
                                Continue with Google
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import store from '@/store/index.js'

export default {
    el: '#app',
    computed: {
        privilege() { return store.state.privilege },
        name() { return store.state.name },
        id() { return store.state.id },
        email() { return store.state.email },
        tokenExp() { return store.state.tokenExp },
    },
    data() {
        return { resp: '' }
    },
    methods: {
        randomString(len = 64) {
            const charset = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~'
            const bytes = new Uint8Array(len)
            window.crypto.getRandomValues(bytes)
            return Array.from(bytes, b => charset[b % charset.length]).join('')
        },
        async sha256(str) {
            const buf = new TextEncoder().encode(str)
            const hash = await window.crypto.subtle.digest('SHA-256', buf)
            return new Uint8Array(hash)
        },
        base64url(bytes) {
            let s = btoa(String.fromCharCode(...bytes))
            return s.replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '')
        },
        async buildPkce() {
            const verifier = this.randomString(64)
            const challengeBytes = await this.sha256(verifier)
            const challenge = this.base64url(challengeBytes)
            return { verifier, challenge }
        },

        async loginWithGoogle() {
            const GOOGLE_AUTH_URL = 'https://accounts.google.com/o/oauth2/v2/auth'
            const clientId = process.env.VUE_APP_GOOGLE_CLIENT_ID 
            const redirectUri = process.env.VUE_APP_OAUTH_REDIRECT_URI || `${window.location.origin}/admin/callback`
            const scope = 'openid email profile'

            const { verifier, challenge } = await this.buildPkce()
            const state = this.base64url(window.crypto.getRandomValues(new Uint8Array(16)))
            const nonce = this.base64url(window.crypto.getRandomValues(new Uint8Array(16)))

            sessionStorage.setItem('pkce_verifier', verifier)
            sessionStorage.setItem('oauth_state', state)
            sessionStorage.setItem('oauth_nonce', nonce)

            const params = new URLSearchParams({
                client_id: clientId,
                redirect_uri: redirectUri,
                response_type: 'code',
                scope,
                state,
                nonce,
                code_challenge: challenge,
                code_challenge_method: 'S256',
                hosted_domain: 'kset.org',
                prompt: 'select_account',
            })

            window.location.href = `${GOOGLE_AUTH_URL}?${params.toString()}`
        },
    },
    mounted() {
    },
}
</script>

<style>
#signin_button {
    text-align: center;
    justify-content: center;
    align-items: center;
}
</style>
