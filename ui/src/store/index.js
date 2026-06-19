import { createStore } from "vuex";
import createPersistedState from "vuex-persistedstate";
import visibilityStore from "./visibilityStore";

export default createStore({
  state: {
    id: "",
    name: "",
    email: "",
    privilege: "",
    role: "",
    tokenExp: 10000000000000000,
    accessToken: "",
    refreshToken: "",
  },
  plugins: [createPersistedState({ storage: window.sessionStorage })],
  mutations: {
    setId(state, value) {
      state.id = value;
    },
    setName(state, value) {
      state.name = value;
    },
    setEmail(state, value) {
      state.email = value;
    },
    setPrivilege(state, value) {
      state.privilege = value;
    },
    setRole(state, value) {
      state.role = value;
    },
    setTokenExp(state, value) {
      state.tokenExp = value;
    },
    setAccessToken(state, value) {
      state.accessToken = value;
    },
    setRefreshToken(state, value) {
      state.refreshToken = value;
    },
    clearAuth(state) {
      state.id = "";
      state.name = "";
      state.email = "";
      state.privilege = "";
      state.role = "";
      state.tokenExp = 10000000000000000;
      state.accessToken = "";
      state.refreshToken = "";
    },
  },
  getters: {
    hasRole: (state) => (role) => state.role === role,
    hasAnyRole:
      (state) =>
      (...roles) =>
        roles.includes(state.role),
  },
  modules: {
    visibilityStore,
  },
});
