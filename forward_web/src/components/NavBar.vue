<template>
  <b-navbar toggleable="lg" type="dark" variant="dark">
    <b-navbar-brand class="font-weight-bold">
      Demodraft
    </b-navbar-brand>

    <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
    
    <b-collapse id="nav-collapse" is-nav align="center">
      <b-navbar-nav>
        <div class="not-logout">
          <b-nav-item :to="{ name: 'policies-page' }" v-if="isLoggedIn">
            Policies
          </b-nav-item>

          <b-nav-item :to="{ name: 'politician-page' }" v-if="isLoggedIn">
            Politicians
          </b-nav-item>

          <b-nav-item :to="{ name: 'about-page' }" v-if="isLoggedIn">
            About
          </b-nav-item>

          <b-nav-item :to="{ name: 'campaign-page' }" v-if="isLoggedIn">
            <span>Campaign</span>
          </b-nav-item>
        </div>

        <b-nav-item class="logout" v-if="isLoggedIn" @click="logout">
          Logout
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
  padding: 12px 12px;

  @media screen and (min-width: 769px) {
    height: 75px;
    padding: 0 12px;
  }

  .navbar-nav {
    margin: 0 auto;
    height: 100%;

    @media screen and (min-width: 769px) {
      .not-logout {
        display: flex;
        height: 100%;
      }

      .logout {
        position: absolute;
        right: 0;
        padding: 0;
        margin: 0;
      }
    }

    .nav-item {
      display: flex;
      width: 125px;
      font-size: 1.2rem;
      letter-spacing: 0.05rem;

      @media screen and (min-width: 769px) {
        height: 100%;
      }

      a {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 100%;
        color: white;
      }

      .router-link-exact-active {
        border-bottom: 2px solid white;
      }
    }
  }

  .navbar-brand {
    font-size: 1.4rem;
    letter-spacing: 1px;
    margin: 0;
  }

  #nav-collapse {
    @media screen and (min-width: 769px) {
      height: 100%;
    }
    .navbar-nav {
      align-items: center;
    }
  }
}
</style>
