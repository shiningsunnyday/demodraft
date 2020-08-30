import Vue from 'vue';
import App from './App.vue';
import router from './_router/router';
import { store } from './_stores/store';
import Axios from 'axios';

import { BootstrapVue } from 'bootstrap-vue';
import './style.scss';

// to access axios across all components
// can use this.$http to directly call axios
Vue.prototype.$http = Axios;
const token = localStorage.getItem('token');

if (token) {
  Vue.prototype.$http.defaults.headers.common['Authorization'] = token;
}
Vue.config.productionTip = false;
Vue.use(BootstrapVue);

new Vue({
  router,
  store,
  render: (h) => h(App),
}).$mount('#app');
