import Vue from "vue";
import Vuex from "vuex";
import createPersistedState from "vuex-persistedstate";
import { userStore } from '@/_stores/modules/user.js';

Vue.use(Vuex);

const userState = createPersistedState({
  paths: ['userStore'],
  storage: window.sessionStorage,
});

// utilize mapstate in components in the future
export const store = new Vuex.Store({
  modules: {
    userStore
  },
  plugins: [userState],
});
