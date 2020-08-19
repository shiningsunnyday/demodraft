<template>
  <b-navbar toggleable="lg" type="dark" variant="dark">
    <b-navbar-brand class="font-weight-bold">
      Demodraft
    </b-navbar-brand>

    <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

    <b-collapse id="nav-collapse" is-nav align="center">
      <b-navbar-nav class="navbar__desktop-navbar">
        <b-nav-item
          :to="{ name: 'policies-page' }"
          class="navbar__link"
          v-if="isLoggedIn"
        >
          Policies
        </b-nav-item>

        <b-nav-item
          :to="{ name: 'politician-page' }"
          class="navbar__link"
          v-if="isLoggedIn"
        >
          Politicians
        </b-nav-item>

        <b-nav-item
          :to="{ name: 'about-page' }"
          class="navbar__link"
          v-if="isLoggedIn"
        >
          About
        </b-nav-item>

        <b-nav-item
          :to="{ name: 'campaign-page' }"
          class="navbar__link"
          v-if="isLoggedIn"
        >
          <span>Campaign</span>
        </b-nav-item>

        <b-nav-item class="navbar__link" v-if="isLoggedIn" @click="logout">
          Logout
        </b-nav-item>

        <b-nav-item
          :to="{ name: 'login-page' }"
          class="navbar__link"
          v-if="!isLoggedIn"
        >
          <span>Login</span>
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
  font-size: 1.2rem;
  height: 100% !important;

  &__link {
    padding: 0.5rem 2rem;

    .nav-link {
      color: white !important;

      &:hover {
        color: greenyellow !important;
      }
    }
  }

  &__desktop-navbar {
    margin: 0 auto;
  }
}
</style>
