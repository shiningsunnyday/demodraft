<template>
  <div class="login">
    <h1 class="login__title">Login</h1>
    <BForm class="login__form" @submit.prevent="handleSubmit">
      <BFormGroup id="username-group" label="Username:" label-for="username">
        <BFormInput
          id="username"
          v-model="user.username"
          type="text"
          required
        />
      </BFormGroup>

      <BFormGroup id="password-group" label="Password:" label-for="password">
        <BFormInput
          id="password"
          v-model="user.password"
          type="password"
          required
        />
      </BFormGroup>
      <div class="login__footer">
        <b-button v-if="isLoading" disabled>
          <b-spinner small></b-spinner>Submit
        </b-button>
        <BButton v-else type="submit" variant="primary">Submit</BButton>
        <router-link :to="{ name: 'signup' }" class="login__link">
          Don't have an account? Sign up!
        </router-link>
      </div>
    </BForm>
  </div>
</template>

<script>
import { BButton, BForm, BFormGroup, BFormInput } from 'bootstrap-vue';

export default {
  name: 'login-page',
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
        campaignPending: false,
      },
      isLoading: false,
    };
  },
  methods: {
    async handleSubmit() {
      const { username, email, password, campaignPending } = this.user;
      this.isLoading = true;
      try {
        await this.$store.dispatch('login', {
          username,
          password,
          campaignPending,
        });
        this.$router.push('/policies');
      } catch (error) {
        console.log(error);
      }
      this.isLoading = false;
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
    .btn {
      display: flex;
      justify-content: center;
      align-items: center;
      span {
        margin-right: 5px;
      }
    }
  }

  &__link {
    font-size: 11px;
  }
}
</style>
