import Vue from "vue";
import Vuex from "vuex";
import axios from "axios";
import createPersistedState from "vuex-persistedstate";
import * as Config from '../config.json';

Vue.use(Vuex);

export const store = new Vuex.Store({
  plugins: [
    createPersistedState({
      storage: window.localStorage, // temporary
    }),
  ],
  state: {
    status: "",
    token: localStorage.getItem("token") || "",
    user: {}, // holds username, email, campaignLaunchStatus
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
    campaignStatusMutation(state) {
      state.user.campaignLaunchStatus = !state.user.campaignLaunchStatus;
    },
  },
  actions: {
    /**
     * @param {Object} user - Holds username, password, campaignLaunchStatus
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
          const { username, email, password } = response.data;
          // temp token
          const token = Buffer.from(`${username}:${password}`, 'utf8').toString('base64');
          // remove campaignLaunchStatus after backend established
          const authUser = {
            username: username,
            email: email,
            campaignLaunchStatus: user.campaignLaunchStatus,
          };
          const stateData = { token: token, user: authUser };
          localStorage.setItem("token", token);
          // axios.defaults.headers.common["Authorization"] = token;
          commit("auth_success", stateData);
        }
      } catch(error) {
        commit("auth_error");
        localStorage.removeItem("token");
        alert(`Incorrect credentials. Try again?`);
        console.error(error.message);
      }
    },
    /**
     * @param {Object} user - Holds username, email, password, campaignLaunchStatus
     */
    async register({ commit }, user) {
      const userData = {
        username: user.username,
        email: user.email,
        password: user.password,
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
          const { username, email, password } = response.data;
          // temp token
          const token = Buffer.from(`${username}:${password}`, 'utf8').toString('base64'); 
          // remove campaignLaunchStatus after backend established
          const newUser = {
            username: username,
            email: email,
            campaignLaunchStatus: user.campaignLaunchStatus,
          };
          const stateData = { token: token, user: newUser };
          localStorage.setItem("token", token);
          // axios.defaults.headers.common["Authorization"] = token;
          commit("auth_success", stateData);
        }
      } catch(error) {
        commit("auth_error");
        localStorage.removeItem("token");
        alert(`Incorrect credentials. Try again?`);
        console.error(error.message);
      }
    },
    logout({ commit }) {
      return new Promise((resolve, reject) => {
        commit("logout");
        localStorage.removeItem("token");
        // delete axios.defaults.headers.common["Authorization"];
        resolve();
      });
    },
    changeCampaignStatus({ commit }) {
      commit("campaignStatusMutation");
    },
  },
  getters: {
    isLoggedIn: (state) => !!state.token,
    authStatus: (state) => state.status,
    username: (state) => state.user.username,
    userCampaignStatus: (state) => state.user.campaignLaunchStatus,
  },
});
