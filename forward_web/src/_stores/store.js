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
          console.log(response.status);

          if (response.status == 204) {
            const { username, email, password, approved, politician_id } = response.data;
            // temp token
            const token = Buffer.from(`${username}:${password}`, 'utf8').toString('base64');
            const authUser = {
              username: username,
              password: password, // security risk, will need to use session cookies/JWT
              email: email,
              approved: approved,
              isMod: false,
              politician_id: politician_id,
              campaignPending: user.campaignPending,
            };
            const stateData = { token: token, user: authUser };
            sessionStorage.setItem("token", token);
            // axios.defaults.headers.common["Authorization"] = token;
            commit("auth_success", stateData);
          } else {
            const { username, email, password, is_mod } = response.data;
            console.log(is_mod);
            // temp token
            const token = Buffer.from(`${username}:${password}`, 'utf8').toString('base64');
            const authUser = {
              username: username,
              password: password, // security risk, will need to use session cookies/JWT
              email: email,
              isMod: is_mod
            };
            const stateData = { token: token, user: authUser };
            sessionStorage.setItem("token", token);
            // axios.defaults.headers.common["Authorization"] = token;
            commit("auth_success", stateData);
          }
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
          const newUser = {
            username: username,
            email: email,
            password: password, // security risk, will need to use session cookies/JWT
            campaignPending: user.campaignPending,
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
    password: (state) => state.user.password, // security risk, will need to use session cookies/JWT
    getUserInfo: (state) => state.user,
  },
});
