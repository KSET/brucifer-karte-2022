import { createStore } from "vuex";
import createPersistedState from "vuex-persistedstate";
import { publicApi } from "@/plugins/publicApi";

export default createStore({
  state: {
    COMINGSOON_VISIBILITY: false,
    LINEUP_VISIBILITY: false,
    SPONSORS_VISIBILITY: false,
    CJENIK_VISIBILITY: false,
    SATNICA_VISIBILITY: false,
    TLOCRT_VISIBILITY: false,
    ULAZNICA_VISIBILITY: false,
    TIMER_VISIBILITY: false,
    IGRICA_VISIBILITY: false,
    TIMER_TIME: "",
    SPONSORS_INPUT_TIME: "",
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
    setIGRICA_VISIBILITY(state, value) {
      state.IGRICA_VISIBILITY = value;
    },
    setTIMER_TIME(state, value) {
      state.TIMER_TIME = value;
    },
    setSPONSORS_INPUT_TIME(state, value) {
      state.SPONSORS_INPUT_TIME = value;
    },
  },
  actions: {
    async fetchVisibilityData({ commit }) {
      try {
        const response = await publicApi.get(
          `/visibility/`
        );
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
      } catch (error) {
        console.error("Failed to fetch visibility data:", error);
      }
    },
  },
});
