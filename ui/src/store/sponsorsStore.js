import { createStore } from 'vuex'
import { api } from '@/plugins/api'
import { publicApi } from '@/plugins/publicApi'

export default createStore({
    state: {
        list: [],
        item: null,
        loading: false,
        error: null,
    },

    getters: {
        list: (s) => s.list,
        item: (s) => s.item,
        loading: (s) => s.loading,
        error: (s) => s.error,
    },

    mutations: {
        SET_LOADING(state, v) { state.loading = v },
        SET_ERROR(state, e) { state.error = e },

        SET_LIST(state, rows) { state.list = Array.isArray(rows) ? rows : [] },
        CLEAR_LIST(state) { state.list = [] },

        SET_ITEM(state, payload) { state.item = payload || null },
        CLEAR_ITEM(state) { state.item = null },

        UPSERT_LIST_ITEM(state, payload) {
            if (!payload) return
            const idx = state.list.findIndex(x => x.id === payload.id)
            if (idx >= 0) state.list.splice(idx, 1, payload)
            else state.list.push(payload)
        },

        REMOVE_LIST_ITEM(state, id) {
            state.list = state.list.filter(x => x.id !== id)
            if (state.item?.id === id) state.item = null
        },
    },

    actions: {
        // --- ADMIN (auth) ---
        async fetchAll({ commit }) {
            commit('SET_LOADING', true); commit('SET_ERROR', null)
            try {
                const { data } = await api.get('/sponsors/', {
                    params: { ordering: 'order' },
                })
                commit('SET_LIST', data)
                return data
            } catch (e) {
                commit('SET_ERROR', e); throw e
            } finally {
                commit('SET_LOADING', false)
            }
        },

        async fetchBySlug({ commit }, slug) {
            commit('SET_LOADING', true); commit('SET_ERROR', null)
            try {
                const { data } = await api.get('/sponsors/', {
                    params: { search: slug, search_fields: 'slug' },
                })
                const found = Array.isArray(data) && data.length ? data[0] : null
                commit('SET_ITEM', found)
                return found
            } catch (e) {
                commit('SET_ERROR', e); throw e
            } finally {
                commit('SET_LOADING', false)
            }
        },

        async create({ commit, state }, formData) {
            commit('SET_LOADING', true); commit('SET_ERROR', null)
            try {
                const { data } = await api.post('/sponsors/', formData, {
                    headers: { 'Content-Type': 'multipart/form-data' },
                })
                commit('SET_ITEM', data)
                if (state.list.length) commit('UPSERT_LIST_ITEM', data)
                return data
            } catch (e) {
                commit('SET_ERROR', e); throw e
            } finally {
                commit('SET_LOADING', false)
            }
        },

        async update({ commit, state }, { id, formData }) {
            commit('SET_LOADING', true); commit('SET_ERROR', null)
            try {
                const { data } = await api.put(`/sponsors/${id}/`, formData, {
                    headers: { 'Content-Type': 'multipart/form-data' },
                })
                commit('SET_ITEM', data)
                if (state.list.length) commit('UPSERT_LIST_ITEM', data)
                return data
            } catch (e) {
                commit('SET_ERROR', e); throw e
            } finally {
                commit('SET_LOADING', false)
            }
        },

        async remove({ commit }, id) {
            commit('SET_LOADING', true); commit('SET_ERROR', null)
            try {
                await api.delete(`/sponsors/${id}/`)
                commit('REMOVE_LIST_ITEM', id)
            } catch (e) {
                commit('SET_ERROR', e); throw e
            } finally {
                commit('SET_LOADING', false)
            }
        },

        // [{ id, order }, ...]
        async reorder({ commit }, items) {
            commit('SET_LOADING', true); commit('SET_ERROR', null)
            try {
                await api.post('/sponsors/reorder/', items)
            } catch (e) {
                commit('SET_ERROR', e); throw e
            } finally {
                commit('SET_LOADING', false)
            }
        },

        // --- PUBLIC (no auth, visible only) ---
        async fetchVisible({ commit }) {
            commit('SET_LOADING', true); commit('SET_ERROR', null)
            try {
                const { data } = await publicApi.get('/public/sponsors/', {
                    params: { ordering: 'order' },
                })
                commit('SET_LIST', data)
                return data
            } catch (e) {
                commit('SET_ERROR', e); throw e
            } finally {
                commit('SET_LOADING', false)
            }
        },
    },
})
