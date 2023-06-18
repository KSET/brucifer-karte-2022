import { createStore } from "vuex";
import createPersistedState from "vuex-persistedstate";
import axios from "axios";

export default createStore({
  state: {
    translations: {},
    translationsTable: {},
  },
  plugins: [createPersistedState()],
  mutations: {
    settranslations(state, value) {
      state.translations = value;
    },
    settranslationsTable(state, value) {
      state.translationsTable = value;
    },
  },
  actions: {
    async fetchTranslations({ commit }) {
      return axios
        .get(`${process.env.VUE_APP_BASE_URL}/translations/?ordering=key`)
        .then((response) => {
          commit("settranslationsTable", response.data);

          const transformedJson = {};

          response.data.forEach((item) => {
            const [key, subKey] = item.key.split(".");

            if (!transformedJson[key]) {
              transformedJson[key] = {};
            }

            transformedJson[key][subKey] = item.value;
          });
          commit("settranslations", transformedJson);
          console.log(transformedJson);
        })
        .catch((error) => {
          console.error("Failed to fetch tanslations data:", error);
        });
    },
  },
});
