<template>
  <div id="app">
    <NavBar :campaignLaunchStatus="campaignLaunchStatus" />
    <router-view
      :key="$route.fullPath"
      :campaignLaunchStatus="campaignLaunchStatus"
    />
  </div>
</template>

<script>
import LoginPage from "./views/LoginPage";
import HomePage from "./views/HomePage";
import SignUp from "./views/SignUp";
import PolicyPage from "./views/PolicyPage";
import AboutPage from "./views/AboutPage";
import NavBar from "./components/NavBar";
import PoliticianList from "./components/politicians/PoliticianList";
import PoliticianCard from "./components/politicians/PoliticianCard";
import PoliticianPage from "./views/PoliticianPage";
import CampaignDetails from "./components/launch-campaign/CampaignDetails";
import CampaignRegistration from "./components/launch-campaign/CampaignRegistration";
import CampaignPage from "./views/CampaignPage";

export default {
  name: "App",
  components: {
    AboutPage,
    LoginPage,
    HomePage,
    SignUp,
    NavBar,
    PolicyPage,
    PoliticianList,
    PoliticianCard,
    PoliticianPage,
    CampaignDetails,
    CampaignRegistration,
    CampaignPage,
  },
  data() {
    return {
      // *** Will move campaignLaunchStatus to VueX store ***
      campaignLaunchStatus: false,
    };
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
