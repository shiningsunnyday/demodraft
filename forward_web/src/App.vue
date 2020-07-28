<template>
  <div id="app">
    <nav>
      <router-link to="/">Home</router-link>
      <router-link to="/login">Login</router-link>
      <router-link to="/signup">Sign Up</router-link>
    </nav>

    <router-view />
  </div>
</template>

<script>
import LoginView from "./views/LoginView";
import HomeView from './views/HomeView';
import SignUpView from './views/SignUpView';

export default {
  name: "App",
  components: {
    LoginView,
    HomeView,
    SignUpView
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

.politician-list {
  list-style: none;
  padding: 0;
}

nav {
  display: flex;
  justify-content: space-between;
  width: 400px;
  margin: 20px auto;
}
</style>
