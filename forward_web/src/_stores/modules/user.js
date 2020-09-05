import { ApiUtil } from '@/_utils/api-utils.js';

export const userStore = {
  state: {
    status: '',
    token: sessionStorage.getItem('token') || '',
    user: {},
  },
  mutations: {
    auth_request(state) {
      state.status = 'loading';
    },
    auth_success(state, data) {
      state.status = 'success';
      state.user = data.user;
      state.token = data.token;
    },
    auth_error(state) {
      state.status = 'error';
    },
    logout(state) {
      state.status = '';
      state.token = '';
    },
    campaignPendingMutation(state) {
      state.user.campaignPending = !state.user.campaignPending;
    },
  },
  actions: {
    async login({ commit }, user) {
      try {
        commit('auth_request');
        const authUser = await ApiUtil.login(user);
        const token = Buffer.from(`${username}:${password}`, 'utf8').toString('base64');
        const stateData = { token: token, user: authUser };
        sessionStorage.setItem("token", token);
        // axios.defaults.headers.common["Authorization"] = token;
        commit('auth_success', stateData);
      } catch (error) {
        commit('auth_error');
        sessionStorage.clear();
        sessionStorage.removeItem('token');
        alert(`Incorrect credentials. Try again?`);
        console.log(error.message);
      }
    },
    async register({ commit }, user) {
      try {
        commit('auth_request');
        const authUser = await ApiUtil.signUp(user);
        const token = Buffer.from(`${username}:${password}`, 'utf8').toString('base64');
        const stateData = { token: token, user: authUser };
        sessionStorage.setItem("token", token);
        // axios.defaults.headers.common["Authorization"] = token;
        commit('auth_success', stateData);
      } catch (error) {
        commit('auth_error');
        sessionStorage.clear();
        sessionStorage.removeItem('token');
        alert(`There was a problem registering your account.`);
        console.log(error.message);
      }
    },
    logout({ commit }) {
      commit('logout');
      sessionStorage.clear();
      // delete axios.defaults.headers.common["Authorization"];
    },
    changeCampaignPending({ commit }) {
      commit('campaignPendingMutation');
    },
  },
  getters: {
    isLoggedIn: (state) => !!state.token,
    authStatus: (state) => state.status,
    username: (state) => state.user.username,
    password: (state) => state.user.password,
    getUserInfo: (state) => state.user,
  },
};
