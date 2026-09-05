import { createStore } from "vuex";
import createPersistedState from "vuex-persistedstate";
import { publicApi } from "@/plugins/publicApi";

export default createStore({
  state: {
    translations: {},
    translationsTable: {},
  },
  plugins: [createPersistedState({ key: "brucifer.translations" })],
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
      try {
        const response = await publicApi.get("/translations/?ordering=key");
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
      } catch (error) {
        console.error("Failed to fetch translations data:", error);
      }
    },
  },
});
