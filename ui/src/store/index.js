import { createStore } from "vuex";
import createPersistedState from "vuex-persistedstate";

// this.$store.state.privilege

export default createStore({
  state: {
    id: "",
    name: "",
    email: "",
    privilege: "",
    tokenExp: 10000000000000000,

    reroutePage: 0,
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
    setreroutePage(state, value) {
      state.reroutePage = value;
    },
  },
});
