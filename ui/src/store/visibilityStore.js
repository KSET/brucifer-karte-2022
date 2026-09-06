import { createStore } from "vuex";
import createPersistedState from "vuex-persistedstate";
import { publicApi } from "@/plugins/publicApi";

let inFlight = null;

const TIME_KEYS = new Set(["TIMER_TIME", "SPONSORS_INPUT_TIME"]);

const mutations = {
  setVISIBILITY_LOADED(state, value) {
    state.VISIBILITY_LOADED = value;
  },
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
  setBRUCOSI_VISIBILITY(state, value) {
    state.BRUCOSI_VISIBILITY = value;
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
};

export default createStore({
  state: {
    VISIBILITY_LOADED: false,
    COMINGSOON_VISIBILITY: false,
    LINEUP_VISIBILITY: false,
    SPONSORS_VISIBILITY: false,
    CJENIK_VISIBILITY: false,
    SATNICA_VISIBILITY: false,
    TLOCRT_VISIBILITY: false,
    ULAZNICA_VISIBILITY: false,
    BRUCOSI_VISIBILITY: false,
    TIMER_VISIBILITY: false,
    IGRICA_VISIBILITY: false,
    TIMER_TIME: null,
    SPONSORS_INPUT_TIME: null,
  },
  plugins: [
    createPersistedState({
      key: "brucifer.visibility",
      reducer: (state) => {
        const { VISIBILITY_LOADED, ...persisted } = state;
        return persisted;
      },
    }),
  ],
  mutations,
  getters: {
    sponsorsInputClosed: (state) => {
      if (!state.SPONSORS_INPUT_TIME) return false;
      const deadline = new Date(state.SPONSORS_INPUT_TIME).getTime();
      return !Number.isNaN(deadline) && Date.now() > deadline;
    },
  },
  actions: {
    async fetchVisibilityData({ commit, state }, { force = false } = {}) {
      if (!force) {
        if (inFlight) return inFlight;
        if (state.VISIBILITY_LOADED) return Promise.resolve();
      }

      inFlight = (async () => {
        try {
          const response = await publicApi.get(
            `/visibility/`
          );

          for (const row of response.data) {
            const mutationName = `set${row.name}`;
            if (!Object.prototype.hasOwnProperty.call(mutations, mutationName)) {
              continue;
            }
            commit(
              mutationName,
              TIME_KEYS.has(row.name) ? row.time ?? null : row.visible
            );
          }
        } catch (error) {
          console.error("Failed to fetch visibility data:", error);
        } finally {
          commit("setVISIBILITY_LOADED", true);
          inFlight = null;
        }
      })();

      return inFlight;
    },
  },
});
