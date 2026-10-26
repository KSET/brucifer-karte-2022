import { createStore } from "vuex";

export default createStore({
  state: {
    name: "",
    email: "",
    role: "",
    accessToken: "",
  },
  mutations: {
    setUser(state, user) {
      state.name = user.name;
      state.email = user.email;
      state.role = user.role;
    },
    setAccessToken(state, value) {
      state.accessToken = value;
    },
    clearAuth(state) {
      state.name = "";
      state.email = "";
      state.role = "";
      state.accessToken = "";
    },
  },
  getters: {
    isLoggedIn: (state) => state.accessToken !== "",
    hasRole: (state) => (role) => state.role === role,
    hasAnyRole:
      (state) =>
      (...roles) =>
        roles.includes(state.role),
  },
});
