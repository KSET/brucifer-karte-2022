import { createStore } from "vuex";
import createPersistedState from "vuex-persistedstate";
import visibilityStore from "./visibilityStore";

export default createStore({
  state: {
    id: "",
    name: "",
    email: "",
    privilege: "",
    tokenExp: 10000000000000000,
    accessToken: "",
    refreshToken: "",
  },
  plugins: [createPersistedState()],
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
      state.tokenExp = 10000000000000000;
      state.accessToken = "";
      state.refreshToken = "";
    },
  },
  modules: {
    visibilityStore,
  },
});
