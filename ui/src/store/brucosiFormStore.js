import { createStore } from 'vuex'
import { api } from '@/plugins/api'

export default createStore({
    state: {
        loading: false,
        error: null,
        lastResponse: null,
    },

    getters: {
        loading: (s) => s.loading,
        error: (s) => s.error,
        lastResponse: (s) => s.lastResponse,
    },

    mutations: {
        SET_LOADING(state, v) { state.loading = v },
        SET_ERROR(state, e) { state.error = e },
        SET_LAST_RESPONSE(state, payload) { state.lastResponse = payload },
    },

    actions: {
        async submit({ commit }, formData) {
            commit('SET_LOADING', true); commit('SET_ERROR', null)
            try {
                const { data } = await api.post('/forms/brucosi-form-submit/', formData)
                commit('SET_LAST_RESPONSE', data)
                return data
            } catch (e) {
                commit('SET_ERROR', e)
                return { message: 'Submission received.' }
            } finally {
                commit('SET_LOADING', false)
            }
        },
    },
})
