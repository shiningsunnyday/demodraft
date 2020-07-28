<template>
  <div class="login">
    <h1 class="login__title">Login</h1>
    <b-form class=login__form>
      <b-form-group
        id="email-group"
        label="Email address:"
        label-for="email"
      >
        <b-form-input
          id="email"
          v-model="form.email"
          type="email"
          required
          placeholder="Enter email"
        ></b-form-input>
      </b-form-group>

      <b-form-group id="password-group" label="Password" label-for="password">
        <b-form-input
          id="password"
          v-model="form.password"
          type="password"
          required
        ></b-form-input>
      </b-form-group>
      <div class="login__footer">
        <b-button type="submit" variant="primary">Submit</b-button>
        <router-link to="/signup" class="login__link">
          Don't have an account? Sign up!
        </router-link>
      </div>
    </b-form>
  </div>
</template>

<script>
export default {
  name: 'LoginView',
  data() {
    return {
      form: {
        email: '',
        password: '',
      },
    };
  },
};
</script>

<style lang="scss" scoped>
.login {
  &__title {
    text-align: center;
    margin-bottom: 2rem;
  }

  &__form {
    max-width: 310px;
    margin: 0 auto;
  }

  &__footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  &__link {
    font-size: 12px;
  }
}
</style>
