<template>
  <b-navbar toggleable="lg" type="dark" variant="dark">
    <b-navbar-brand>
      <router-link to="/" class="navbar__link">Home</router-link>
    </b-navbar-brand>
    <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
    <b-collapse id="nav-collapse" is-nav="">
      <b-navbar-nav>
        <b-nav-item>
          <router-link to="/login" class="navbar__link">
            Login
          </router-link>
        </b-nav-item>
      </b-navbar-nav>
    </b-collapse>
  </b-navbar>
</template>

<script>
export default {
  name: 'NavBar',
};
</script>

<style lang="scss" scoped>
.navbar {
  margin-bottom: 2rem;
  box-shadow: 0 3px 6px rgba(0,0,0,0.16), 0 3px 6px rgba(0,0,0,0.23);
  &__link {
    color: white;

    &:hover {
      color: greenyellow;
    }
  }
}
</style>
