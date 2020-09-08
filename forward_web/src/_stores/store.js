import Vue from "vue";
import Vuex from "vuex";
//import createPersistedState from "vuex-persistedstate";
import { userStore } from '@/_stores/modules/user.js';
import { politicianStore } from '@/_stores/modules/politician.js';

Vue.use(Vuex);

// const allState = createPersistedState({
//   paths: ['userStore', 'politicianStore'],
//   storage: window.sessionStorage,
//   reducer: (vuexState) => {
//   }
// });

// utilize mapstate in components in the future
export const store = new Vuex.Store({
  modules: {
    userStore,
    politicianStore,
  },
  // plugins: [allState],
});
