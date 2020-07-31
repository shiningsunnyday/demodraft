<template>
  <div class="login">
    <h1 class="login__title">Login</h1>
    <BForm class=login__form @submit.prevent="handleSubmit">
      <BFormGroup
        id="username-group"
        label="Username:"
        label-for="username"
      >
        <BFormInput
          id="username"
          v-model="user.username"
          type="text"
          required
        />
      </BFormGroup>

      <BFormGroup id="password-group" label="Password" label-for="password">
        <BFormInput
          id="password"
          v-model="user.password"
          type="password"
          required
        />
      </BFormGroup>
      <div class="login__footer">
        <BButton type="submit" variant="primary">Submit</BButton>
        <router-link to="/signup" class="login__link">
          Don't have an account? Sign up!
        </router-link>
      </div>
    </BForm>
  </div>
</template>

<script>
import { BButton, BForm, BFormGroup, BFormInput } from 'bootstrap-vue';
import axios from 'axios';
export default {
  name: 'LoginView',
  components: {
    'b-button': BButton,
    'b-form': BForm,
    'b-form-group': BFormGroup,
    'b-form-input': BFormInput,
  },
  data() {
    return {
      user: {
        username: '',
        email: '',
        password: '',
      },
    };
  },
  methods: {
    async handleSubmit() {
      const { username, email, password } = this.user;
      this.$store
        .dispatch('login', { username, password })
        .then(() => this.$router.push('/'))
        .catch((err) => console.log(err));
    },
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
