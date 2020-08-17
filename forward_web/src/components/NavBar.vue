<template>
  <b-navbar toggleable="lg" type="dark" variant="dark">
    <b-navbar-brand>
      <router-link :to="{ name: 'about-page' }" class="navbar__link" v-if="!isLoggedIn">
        About
      </router-link>

      <router-link :to="{ name: 'home-page' }" class="navbar__link" v-else>
        Home
      </router-link>
    </b-navbar-brand>

    <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

    <b-collapse id="nav-collapse" is-nav="">
      <b-navbar-nav>
        <!-- <b-nav-item v-if="isLoggedIn">
          <router-link :to="{ name: 'about-page' }" class="navbar__link">
            About
          </router-link>
        </b-nav-item> -->

        <b-nav-item v-if="isLoggedIn">
          <router-link :to="{ name: 'politician-page' }" class="navbar__link">
            Politicians
          </router-link>
        </b-nav-item>

        <b-nav-item v-if="isLoggedIn">
          <router-link :to="{ name: 'campaign-page' }" class="navbar__link">
            <span>Campaign</span>
          </router-link>
        </b-nav-item>

        <b-nav-item v-if="isLoggedIn" @click="logout">
          Logout
        </b-nav-item>

        <b-nav-item v-if="!isLoggedIn">
          <router-link :to="{ name: 'login-page' }" class="navbar__link">
            <span>Login</span>
          </router-link>
        </b-nav-item>
      </b-navbar-nav>
    </b-collapse>
  </b-navbar>
</template>

<script>
export default {
  name: 'nav-bar',
  computed: {
    isLoggedIn() {
      return this.$store.getters.isLoggedIn;
    },
  },
  methods: {
    logout() {
      this.$store.dispatch('logout').then(() => {
        this.$router.push('/login');
      });
    },
  },
};
</script>

<style lang="scss" scoped>
.navbar {
  margin-bottom: 2rem;
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.16), 0 3px 6px rgba(0, 0, 0, 0.23);
  &__link {
    color: white;

    &:hover {
      color: greenyellow;
    }
  }
}
</style>
