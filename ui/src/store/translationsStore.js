import { createStore } from "vuex";
import createPersistedState from "vuex-persistedstate";
import axios from "axios";

export default createStore({
  state: {
    translations: {},
  },
  plugins: [createPersistedState()],
  mutations: {
    settranslations(state, value) {
      state.translations = value;
    },
  },
  actions: {
    async fetchTranslations({ commit }) {
      return axios
        .get(`${process.env.VUE_APP_BASE_URL}/translations/`)
        .then((response) => {
          const transformedJson = {};

          response.data.forEach((item) => {
            const [key, subKey] = item.key.split(".");

            if (!transformedJson[key]) {
              transformedJson[key] = {};
            }

            transformedJson[key][subKey] = item.value;
          });
          commit("settranslations", transformedJson);
        })
        .catch((error) => {
          console.error("Failed to fetch tanslations data:", error);
        });
    },
  },
});
