import Vue from 'vue';
import App from './App.vue';
import router from './router/router';
import { store } from './stores/store';
import Axios from 'axios';

import { BootstrapVue } from 'bootstrap-vue';
import 'vue-virtual-scroller/dist/vue-virtual-scroller.css';
import './style.scss';
import VueVirtualScroller from 'vue-virtual-scroller';

// to access axios across all components
// can use this.$http to directly call axios
Vue.prototype.$http = Axios;
const token = localStorage.getItem('token');

if (token) {
  Vue.prototype.$http.defaults.headers.common['Authorization'] = token;
}
Vue.config.productionTip = false;
Vue.use(BootstrapVue);
Vue.use(VueVirtualScroller);

new Vue({
  router,
  store,
  render: (h) => h(App),
}).$mount('#app');
