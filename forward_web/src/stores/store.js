import Vue from "vue";
import Vuex from "vuex";
import axios from "axios";
import createPersistedState from "vuex-persistedstate";

Vue.use(Vuex);

export const store = new Vuex.Store({
  plugins: [
    createPersistedState({
      storage: window.localStorage,
    }),
  ],
  state: {
    status: "",
    token: localStorage.getItem("token") || "",
    user: {},
  },
  mutations: {
    auth_request(state) {
      state.status = "loading";
    },
    auth_success(state, data) {
      // need more testing
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
    login({ commit }, user) {
      return new Promise((resolve, reject) => {
        const userData = {
          username: user.username,
          email: user.email,
          password: user.password,
        };
        commit("auth_request");
        axios({
          url:
            "http://ec2-54-183-146-26.us-west-1.compute.amazonaws.com/login/",
          data: userData,
          method: "post",
          headers: { "content-type": "application/json" },
          auth: {
            username: "demodraft",
            password: "darkmoney",
          },
        })
          .then((resp) => {
            const authString = resp.config.headers.Authorization;
            const token = authString.split(" ")[1];
            // * remove these lines of code once backend is setup to accept campaignLaunchStatus
            const newUser = resp.data;
            newUser.campaignLaunchStatus = user.campaignLaunchStatus;
            // *
            const data = {
              token: token,
              user: newUser,
            };
            localStorage.setItem("token", token);
            axios.defaults.headers.common["Authorization"] = token;
            commit("auth_success", data);
            resolve(resp);
          })
          .catch((err) => {
            commit("auth_error");
            localStorage.removeItem("token");
            alert(`That wasn't correct. Try again?`);
            reject(err);
          });
      });
    },
    register({ commit }, user) {
      return new Promise((resolve, reject) => {
        commit("auth_request");
        const userData = {
          username: user.username,
          email: user.email,
          password: user.password,
        };
        axios({
          url:
            "http://ec2-54-183-146-26.us-west-1.compute.amazonaws.com/signup/",
          data: userData,
          method: "POST",
          headers: { "content-type": "application/json" },
          auth: {
            username: "demodraft",
            password: "darkmoney",
          },
        })
          .then((resp) => {
            const authString = resp.config.headers.Authorization;
            const token = authString.split(" ")[1];
            // * remove these lines of code once backend is setup to accept campaignLaunchStatus
            const newUser = resp.data;
            newUser.campaignLaunchStatus = user.campaignLaunchStatus;
            // *
            const data = {
              token: token,
              user: newUser,
            };
            localStorage.setItem("token", token);
            axios.defaults.headers.common["Authorization"] = token;
            commit("auth_success", data);
            resolve(resp);
          })
          .catch((err) => {
            commit("auth_error");
            localStorage.removeItem("token");
            alert(`Incorrect credentials. Try again?`);
            reject(err);
          });
      });
    },
    logout({ commit }) {
      return new Promise((resolve, reject) => {
        commit("logout");
        localStorage.removeItem("token");
        delete axios.defaults.headers.common["Authorization"];
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
