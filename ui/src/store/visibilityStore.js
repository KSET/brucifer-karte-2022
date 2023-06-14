import { createStore } from "vuex";
import createPersistedState from "vuex-persistedstate";

export default createStore({
  state: {
    COMINGSOON_VISIBILITY: "",
    LINEUP_VISIBILITY: "",
    SPONSORS_VISIBILITY: "",
    CJENIK_VISIBILITY: "",
    SATNICA_VISIBILITY: "",
    TLOCRT_VISIBILITY: "",
    ULAZNICA_VISIBILITY: "",
    TIMER_VISIBILITY: "",
  },
  plugins: [createPersistedState()],
  mutations: {
    setCOMINGSOON_VISIBILITY(state, value) {
      state.COMINGSOON_VISIBILITY = value;
    },
    setLINEUP_VISIBILITY(state, value) {
      state.LINEUP_VISIBILITY = value;
    },
    setSPONSORS_VISIBILITY(state, value) {
      state.SPONSORS_VISIBILITY = value;
    },
    setCJENIK_VISIBILITY(state, value) {
      state.CJENIK_VISIBILITY = value;
    },
    setSATNICA_VISIBILITY(state, value) {
      state.SATNICA_VISIBILITY = value;
    },
    setTLOCRT_VISIBILITY(state, value) {
      state.TIMER_VISIBILITY = value;
    },
    setULAZNICA_VISIBILITY(state, value) {
      state.ULAZNICA_VISIBILITY = value;
    },
    setTIMER_VISIBILITY(state, value) {
      state.TIMER_VISIBILITY = value;
    },
  },
});
