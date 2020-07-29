<template>
  <div id="app">
    <NavBar />
    <router-view />
  </div>
</template>

<script>
import LoginView from './views/LoginView';
import HomeView from './views/HomeView';
import SignUpView from './views/SignUpView';
import PolicyView from './views/PolicyView';
import NavBar from './components/NavBar';

export default {
  name: 'App',
  components: {
    LoginView,
    HomeView,
    SignUpView,
    NavBar,
    PolicyView
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
