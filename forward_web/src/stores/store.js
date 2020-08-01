import Vue from 'vue';
import Vuex from 'vuex';
import axios from 'axios';

Vue.use(Vuex);

export const store = new Vuex.Store({
  state: {
    status: '',
    token: localStorage.getItem('token') || '',
    user: {},
  },
  mutations: {
    auth_request(state) {
      state.status = 'loading';
    },
    auth_success(state, data) { // need more testing
      state.status = 'success';
      state.token = data.token;
      state.user = data.user;
    },
    auth_error(state) {
      state.status = 'error';
    },
    logout(state) {
      state.status = '';
      state.token = '';
    },
  },
  actions: {
    login({ commit }, user) {
      return new Promise((resolve, reject) => {
        commit('auth_request');

        //////
        ////  test data
        // 
        const token = 'token321';
        const data = {
          token: token,
          user: {
            username: 'test',
            password: 'test'
          }
        };
        
        localStorage.setItem('token', token);
        axios.defaults.headers.common['Authorization'] = token;
        commit('auth_success', data);
        resolve(user);
        //
        /// end test data
        ////

        
        // axios({
        //   url: 'http://ec2-54-183-146-26.us-west-1.compute.amazonaws.com/login/',
        //   data: user,
        //   method: 'GET',
        // })
        //   .then((resp) => {
        //     //const token = resp.data.token;
        //     const token = 'token123';
        //     const data = {
        //       token: 'token123', 
        //       user: resp.data
        //     };
        //     localStorage.setItem('token', token);
        //     axios.defaults.headers.common['Authorization'] = token;
        //     commit('auth_success', data);
        //     resolve(resp);
        //   })
        //   .catch((err) => {
        //     commit('auth_error');
        //     localStorage.removeItem('token');
        //     reject(err);
        //   });
      });
    },
    register({ commit }, user) {
      return new Promise((resolve, reject) => {
        commit('auth_request');
        axios({
          url: 'http://ec2-54-183-146-26.us-west-1.compute.amazonaws.com/signup/',
          data: user,
          method: 'POST',
          headers: {'content-type': 'application/json'},
          auth: {
            username: 'admin',
            password: 'password'
          }
        })
          .then((resp) => {
            //const token = resp.data.token;
            const token = 'token123';
            const data = {
              token: 'token123', 
              user: resp.data
            };
            localStorage.setItem('token', token);
            axios.defaults.headers.common['Authorization'] = token;
            commit('auth_success', data);
            console.log(resp);
            resolve(resp);
          })
          .catch((err) => {
            commit('auth_error', err);
            localStorage.removeItem('token');
            reject(err);
          });
      });
    },
    logout({ commit }) {
      return new Promise((resolve, reject) => {
        commit('logout');
        localStorage.removeItem('token');
        delete axios.defaults.headers.common['Authorization'];
        resolve();
      });
    },
  },
  getters: {
    isLoggedIn: (state) => !!state.token,
    authStatus: (state) => state.status,
  },
});
