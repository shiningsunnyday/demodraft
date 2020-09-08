import * as types from '@/_stores/mutation-types';
import { AuthUtil } from '@/_utils/auth-utils.js';

const user = JSON.parse(sessionStorage.getItem('userState'));
export const userStore = {
  state: user
    ? {
        status: {
          loggedIn: true,
        },
        user,
      }
    : {
        status: {
          loggedIn: false,
        },
        user: {},
      },
  mutations: {
    [types.AUTH_SUCCESS]: (state, user) => {
      state.status.loggedIn = true;
      state.user = user;
    },
    [types.AUTH_ERROR]: (state) => {
      state.status.loggedIn = false;
    },
    [types.LOGOUT]: (state) => {
      state.status.loggedIn = false;
      state.user = {};
    },
    [types.SET_CAMPAIGN_PENDING]: (state) => {
      state.user.campaignPending = !state.user.campaignPending;
    },
  },
  actions: {
    login: async ({ commit }, user) => {
      try {
        const authUser = await AuthUtil.login(user);
        sessionStorage.setItem('userState', JSON.stringify(authUser));
        commit(types.AUTH_SUCCESS, authUser);
      } catch (error) {
        commit('auth_error');
        alert(`Incorrect credentials. Try again?`);
        console.log(error.message);
      }
    },
    register: async ({ commit }, user) => {
      try {
        const authUser = await AuthUtil.signUp(user);
        sessionStorage.setItem('userState', JSON.stringify(authUser));
        commit(types.AUTH_SUCCESS, authUser);
      } catch (error) {
        commit('auth_error');
        alert(`There was a problem registering your account.`);
        console.log(error.message);
      }
    },
    logout: ({ commit }) => {
      sessionStorage.removeItem('userState');
      sessionStorage.removeItem('pol_store');
      commit(types.LOGOUT);
    },
    changeCampaignPending: ({ commit }) => {
      commit(types.SET_CAMPAIGN_PENDING);
    },
  },
  getters: {
    isLoggedIn: (state) => state.status.loggedIn,
    authStatus: (state) => state.status,
    username: (state) => state.user.username,
    password: (state) => state.user.password,
    getUserInfo: (state) => state.user,
  },
};
