import { createStore } from "vuex";
import createPersistedState from "vuex-persistedstate";

export default createStore({
  state: {
    comingSoon: "",
    lineup: "",
    sponsors: "",
    cjenik: "",
    satnica: "",
    ulaznica: "",
    timer: "",
  },
  plugins: [createPersistedState()],
  mutations: {
    setComingSoon(state, value) {
      state.comingSoon = value;
    },
    setLineup(state, value) {
      state.lineup = value;
    },
    setSponsors(state, value) {
      state.sponsors = value;
    },
    setCjenik(state, value) {
      state.cjenik = value;
    },
    setSatnica(state, value) {
      state.satnica = value;
    },
    setUlaznica(state, value) {
      state.ulaznica = value;
    },
    setTimer(state, value) {
      state.timer = value;
    },
  },
});
