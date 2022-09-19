import { createStore } from 'vuex'
import createPersistedState from 'vuex-persistedstate'

// this.$store.state.privilege


export default createStore({
  state: {
      id: '',
      name: '',
      email: '',
      privilege: '',
      tokenExp: 10000000000000000,

      updateData: [],
  },
  plugins: [createPersistedState()],
  mutations: {
    setId (state, value) {
      state.id = value
    },
    setName (state, value) {
      state.name = value
    },
    setEmail (state, value) {
      state.email = value
    },
    setPrivilege (state, value) {
      state.privilege = value
    },
    setTokenExp (state, value) {
      state.tokenExp = value
    },
    setupdateData (state, value) {
      state.updateData = value.slice();
    }
  }
});


/*
export default createStore({
  state: {
    count: 0
  },
  plugins: [createPersistedState()],
  mutations: {
    increment: state => state.count++,
    decrement: state => state.count--,
    setto (state, set) {
      state.count = set
    }
  }
});*/