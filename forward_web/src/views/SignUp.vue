<template>
  <div class="signup">
    <h1 class="signup__title">Sign Up</h1>
    <BForm class="signup__form" @submit.prevent="handleSubmit">
      <BFormGroup id="username-group" label="Username:" label-for="username">
        <BFormInput
          id="username"
          v-model="user.username"
          type="text"
          required
        />
      </BFormGroup>

      <BFormGroup
        id="email-group"
        label="Email address:"
        label-for="email"
        description="Please use the same email you subscribed to us on demodraft.org"
      >
        <BFormInput
          id="email"
          v-model="user.email"
          type="email"
          required
        />
      </BFormGroup>

      <BFormGroup
        label="First name:"
        label-for="first"
      >
        <BFormInput
          v-model="user.first"
          type="text"
          required
        />
      </BFormGroup>

      <BFormGroup
        label="Last name:"
        label-for="last"
      >
        <BFormInput
          v-model="user.last"
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

      <BFormGroup id="confirm-password-group" label="Confirm Password:" label-for="confirm-password">
        <BFormInput
          id="confirm-password"
          v-model="user.confirmPassword"
          type="password"
          required
        />
      </BFormGroup>

      <div class="signup__footer">
        <b-button v-if="submitted" disabled class="align">
          <b-spinner small></b-spinner>
          <span>Submit</span>
        </b-button>
        <BButton v-else type="submit" variant="primary">
          Submit
        </BButton>
        <router-link :to="{ name: 'login-page' }" class="signup__link">
          Already have an account? Login!
        </router-link>
      </div>
    </BForm>
  </div>
</template>

<script>
import { BButton, BForm, BFormGroup, BFormInput } from 'bootstrap-vue';

export default {
  name: 'signup',
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
        first: '',
        last: '',
        password: '',
        confirmPassword: '',
        campaignPending: false,
      },
      submitted: false,
    };
  },
  methods: {
    async handleSubmit() {
      this.submitted = true;
      const { username, email, first, last, password, confirmPassword, campaignPending } = this.user;

      if (password !== confirmPassword) {
        alert('Make sure your passwords match');
        return;
      }

      let data = {
        username: username,
        email: email,
        first_name: first,
        last_name: last,
        password: password,
        campaignPending: campaignPending,
      };

      try {
        await this.$store.dispatch('register', data);
        this.$router.push('/');
      } catch (error) {
        console.log('err', error);
      }
      this.submitted = false;
    },
  },
};
</script>

<style lang="scss" scoped>
.signup {
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
.align {
  display: flex;
  align-items: center;
}
</style>
