import Vue from "vue";
import Vuex from "vuex";
import axios from "axios";
import createPersistedState from "vuex-persistedstate";
import * as Config from '../config.json';

Vue.use(Vuex);
// separate into files and modules in the future
// utilize mapstate in components in the future
export const store = new Vuex.Store({
  plugins: [
    createPersistedState({
      storage: window.sessionStorage, // temporary
    }),
  ],
  state: {
    status: "",
    token: sessionStorage.getItem("token") || "",
    user: {}, // holds username, email, password, approved, politician_id, campaignPending
  },
  mutations: {
    auth_request(state) {
      state.status = "loading";
    },
    auth_success(state, data) {
      state.status = "success";
      state.token = data.token;
      state.user = data.user;
    },
    auth_error(state) {
      state.status = "error";
    },
    logout(state) {
      state.status = "";
      state.token = "";
    },
    campaignPendingMutation(state) {
      state.user.campaignPending = !state.user.campaignPending;
    },
    simulateLoginAuth(state, data) {
      state.status = "success";
      state.token = data.token;
      state.user = data.user;
    }
  },
  // all actions are asynchronous
  actions: {
    /**
     * @param {Object} user - Holds username, password, launchStatusTest
     */
    async login({ commit }, user) {
      const userData = {
        username: user.username,
        password: user.password,
      };

      try {
        commit("auth_request");
        const response = await axios({
          method: 'post',
          url: `${Config.API_URL}/login/`,
          data: userData,
          headers: { "content-type": "application/json" },
          auth: Config.API_AUTH
        });
        
        if (response) {
          const { id, username, email, password, approved, first_name, last_name, politician_id, is_mod } = response.data;
          // temp token
          const token = Buffer.from(`${username}:${password}`, 'utf8').toString('base64');
          const authUser = {
            id: id,
            username: username,
            password: password,
            email: email,
            first_name: first_name,
            last_name: last_name,
            approved: approved,
            isMod: response.status === 204 ? false : is_mod,
            politician_id: politician_id,
            campaignPending: user.campaignPending,
          };
          const stateData = { token: token, user: authUser };
          // sessionStorage.setItem("token", token);
          // axios.defaults.headers.common["Authorization"] = token;
          commit("auth_success", stateData);
        }
      } catch(error) {
        commit("auth_error");
        sessionStorage.removeItem("token");
        // sessionStorage.clear();
        alert(`Incorrect credentials. Try again?`);
        console.error(error.message);
      }
    },
    /**
     * @param {Object} user - Holds username, email, password, first_name, last_name, campaignLaunchStatus
     */
    async register({ commit }, user) {
      const userData = {
        username: user.username,
        email: user.email,
        password: user.password,
        first_name: user.first_name,
        last_name: user.last_name
      };

      try {
        commit("auth_request");
        const response = await axios({
          method: 'post',
          url: `${Config.API_URL}/signup/`,
          data: userData,
          headers: { "content-type": "application/json" },
          auth: Config.API_AUTH
        });

        if (response) {
          const { id, username, email, password, first_name, last_name } = response.data;
          // temp token
          const token = Buffer.from(`${username}:${password}`, 'utf8').toString('base64'); 
          const newUser = {
            id: id,
            username: username,
            email: email,
            password: password,
            first_name: first_name,
            last_name: last_name,
            campaignPending: user.campaignPending,
          };
          const stateData = { token: token, user: newUser };
          // sessionStorage.setItem("token", token);
          // axios.defaults.headers.common["Authorization"] = token;
          commit("auth_success", stateData);
        }
      } catch(error) {
        commit("auth_error");
        sessionStorage.removeItem("token");
        alert(`Incorrect credentials. Try again?`);
        console.error(error.message);
      }
    },
    logout({ commit }) {
      return new Promise((resolve, reject) => {
        commit("logout");
        sessionStorage.clear();
        // delete axios.defaults.headers.common["Authorization"];
        resolve();
      });
    },
    changeCampaignPending({ commit }) {
      commit("campaignPendingMutation");
    },
    simulateLogin({ commit }, user) {
      const token = 'token';
      const authUser = {
        username: user.username,
        email: user.email,
        password: user.password,
        campaignPending: user.campaignPending,
        approved: user.approved,
      };
      const stateData = { token: token, user: authUser };
      commit("simulateLoginAuth", stateData);
    }
  },
  getters: {
    isLoggedIn: (state) => !!state.token,
    authStatus: (state) => state.status,
    username: (state) => state.user.username,
    password: (state) => state.user.password,
    getUserInfo: (state) => state.user,
  },
});
