import { createStore } from "vuex";
import createPersistedState from "vuex-persistedstate";
import axios from "axios";

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
      state.TLOCRT_VISIBILITY = value;
    },
    setULAZNICA_VISIBILITY(state, value) {
      state.ULAZNICA_VISIBILITY = value;
    },
    setTIMER_VISIBILITY(state, value) {
      state.TIMER_VISIBILITY = value;
    },
  },
  actions: {
    async fetchVisibilityData({ commit }) {
      return axios
        .get(`${process.env.VUE_APP_BASE_URL}/visibility/`)
        .then((response) => {
          const visibilityResp = response.data.reduce((result, obj) => {
            result[obj.name] = obj.visible;
            return result;
          }, {});

          for (const key in visibilityResp) {
            if (Object.prototype.hasOwnProperty.call(visibilityResp, key)) {
              const value = visibilityResp[key];
              const mutationName = `set${key}`;
              commit(mutationName, value);
            }
          }
        })
        .catch((error) => {
          console.error("Failed to fetch visibility data:", error);
        });
    },
  },
});
