<template>
  <b-navbar toggleable="lg" type="dark" variant="dark">
    <b-navbar-brand class="navbar-brand--mobile">
      Demodraft
    </b-navbar-brand>
    <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

    <b-collapse id="nav-collapse" is-nav>
      <b-navbar-nav>
        <b-navbar-brand>
          Demodraft
        </b-navbar-brand>

        <div class="not-logout" v-if="isLoggedIn">
          <b-nav-item :to="{ name: 'policies-page' }">
            Policies
          </b-nav-item>

          <b-nav-item :to="{ name: 'politician-page' }">
            Politicians
          </b-nav-item>

          <b-nav-item :to="{ name: 'about-page' }">
            About
          </b-nav-item>

          <b-nav-item :to="{ name: 'campaign-page' }">
            <span>Campaign</span>
          </b-nav-item>
        </div>

        <b-nav-item-dropdown class="navbar__user" v-if="isLoggedIn" text="User" right >
          <b-dropdown-item :to="{ name: 'profile-page' }">Profile</b-dropdown-item>
          <b-dropdown-item  @click="handleLogout">Logout</b-dropdown-item>
        </b-nav-item-dropdown>
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
    handleLogout() {
      this.$store.dispatch('logout').then(() => {
        this.$router.push('/login');
      });
    },
  },
};
</script>

<style lang="scss" scoped>
$collapsed-breakpoint: 991px;
$uncollapsed-breakpoint: 992px;

@mixin navbar-no-burger {
  @media screen and (min-width: $uncollapsed-breakpoint) {
    @content;
  }
}

@mixin navbar-burger {
  @media screen and (max-width: $collapsed-breakpoint) {
    @content;
  }
}

.navbar {
  margin-bottom: 2rem;
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.16), 0 3px 6px rgba(0, 0, 0, 0.23);
  padding: 12px 12px;

  @include navbar-no-burger {
    height: 75px;
    padding: 0 12px;
  }

  .navbar-nav {
    display: flex;
    flex-direction: column;
    width: 100%;
    height: 100%;

    @include navbar-no-burger {
      flex-direction: row;
      justify-content: space-between;
      align-items: center;

      .not-logout {
        display: flex;
        height: 100%;
      }
    }

    .nav-item {
      display: flex;
      width: 125px;
      font-size: 1.2rem;
      letter-spacing: 0.05rem;

      a {
        display: flex;
        align-items: center;
        width: 100%;
        color: white;
        
        @include navbar-no-burger {
          justify-content: center;
        }
      }

      .router-link-exact-active {
        border-bottom: 2px solid white;
      }
    }
  }

  .navbar-brand {
    font-size: 1.4rem;
    letter-spacing: 1px;
    font-weight: bold;

    @include navbar-burger {
      display: none;
    }

    &--mobile {
      display: inline-block;
      @include navbar-no-burger {
        display: none;
      }
    }
  }

  .navbar-collapse {
    @include navbar-no-burger {
      height: 100%;
    }
  }
}
</style>
