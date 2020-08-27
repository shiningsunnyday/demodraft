<template>
  <div id="app">
    <NavBar />
    <keep-alive>
      <router-view v-if="$route.meta.keepAlive" :key="$route.fullPath" />
    </keep-alive>
    <router-view v-if="!$route.meta.keepAlive" :key="$route.fullPath" />
  </div>
</template>

<script>
import LoginPage from './views/LoginPage';
import PoliciesPage from './views/PoliciesPage';
import SignUp from './views/SignUp';
import AboutPage from './views/AboutPage';
import NavBar from './components/NavBar';
import PoliticianPage from './views/PoliticianPage';
import CampaignPage from './views/CampaignPage';

export default {
  name: 'App',
  components: {
    AboutPage,
    LoginPage,
    PoliciesPage,
    SignUp,
    NavBar,
    PoliticianPage,
    CampaignPage,
  },
  created() {
    // intercept axios call to check for unauthorized repsonse
    this.$http.interceptors.response.use(undefined, function(err) {
      return new Promise(function(resolve, reject) {
        if (err.status === 401 && err.config && !err.config.__isRetryRequest) {
          this.$store.dispatch('logout');
        }
        throw err;
      });
    });
  },
};
</script>

<style lang="scss">
#app {
  font-family: 'Heebo', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}
</style>
