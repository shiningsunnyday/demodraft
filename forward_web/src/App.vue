<template>
  <div id="app">
    <NavBar />
    <router-view :key='$route.fullPath' />
  </div>
</template>

<script>
import LoginPage from "./views/LoginPage";
import HomePage from "./views/HomePage";
import SignUp from "./views/SignUp";
import PolicyPage from "./views/PolicyPage";
import AboutPage from './views/AboutPage';
import NavBar from "./components/NavBar";
import CommentList from "./components/CommentList";

export default {
  name: "App",
  components: {
    AboutPage,
    LoginPage,
    HomePage,
    SignUp,
    NavBar,
    PolicyPage,
    CommentList,
  },
  created() {
    // intercept axios call to check for unauthorized repsonse
    this.$http.interceptors.response.use(undefined, function(err) {
      return new Promise(function(resolve, reject) {
        if (err.status === 401 && err.config && !err.config.__isRetryRequest) {
          this.$store.dispatch("logout");
        }
        throw err;
      });
    });
  },
};
</script>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}
</style>
