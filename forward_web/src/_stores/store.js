import Vue from "vue";
import Vuex from "vuex";
import axios from "axios";
import createPersistedState from "vuex-persistedstate";
import * as Config from '../config.json';

Vue.use(Vuex);

export const store = new Vuex.Store({
  plugins: [
    createPersistedState({
      storage: window.sessionStorage, // temporary
    }),
  ],
  state: {
    status: "",
    token: sessionStorage.getItem("token") || "",
    user: {}, // holds username, email, password, approved, politician_id, launchStatusTest, submissionStatusTest
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
      state.user.launchStatusTest = !state.user.launchStatusTest;
    },
    submissionStatusMutation(state) {
      state.user.submissionStatusTest = !state.user.submissionStatusTest;
    },
  },
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
          const { username, email, password, approved, politician_id } = response.data;
          // temp token
          const token = Buffer.from(`${username}:${password}`, 'utf8').toString('base64');
          // remove campaignLaunchStatus after backend established
          const authUser = {
            username: username,
            password: password, // security risk, will need to use session cookies/JWT
            email: email,
            approved: approved,
            politician_id: politician_id,
            launchStatusTest: user.launchStatusTest,
            submissionStatusTest: user.submissionStatusTest,
          };
          const stateData = { token: token, user: authUser };
          sessionStorage.setItem("token", token);
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
            password: password, // security risk, will need to use session cookies/JWT
            launchStatusTest: user.launchStatusTest,
            submissionStatusTest: user.submissionStatusTest,
          };
          const stateData = { token: token, user: newUser };
          sessionStorage.setItem("token", token);
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
        sessionStorage.removeItem("token");
        // delete axios.defaults.headers.common["Authorization"];
        resolve();
      });
    },
    changeLaunchStatusTest({ commit }) {
      commit("campaignStatusMutation");
    },
    changeSubmissionStatusTest({ commit }) {
      commit("submissionStatusMutation");
    },
  },
  getters: {
    isLoggedIn: (state) => !!state.token,
    authStatus: (state) => state.status,
    username: (state) => state.user.username,
    password: (state) => state.user.password, // security risk, will need to use session cookies/JWT
    getUserInfo: (state) => state.user,
    userLaunchStatusTest: (state) => state.user.launchStatusTest,
    userSubmissionStatusTest: (state) => state.user.submissionStatusTest,
  },
});
