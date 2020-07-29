<template>
  <div class="signup">
    <h1 class="signup__title">Sign Up</h1>
    <BForm class="signup__form" @submit.prevent="handleSubmit">
      <BFormGroup id="username-group" label="Username" label-for="username">
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
        description="We'll never share your email with anyone else."
      >
        <BFormInput
          id="email"
          v-model="user.email"
          type="email"
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
      
      <div class="signup__footer">
        <BButton type="submit" variant="primary">
          Submit
        </BButton>
        <router-link to="/login" class="signup__link">
          Already have an account? Login!
        </router-link>
      </div>
    </BForm>
  </div>
</template>

<script>
import { BButton, BForm, BFormGroup, BFormInput } from 'bootstrap-vue';
import axios from 'axios';

export default {
  name: 'SignUpView',
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
      submitted: false,
    };
  },
  methods: {
    async handleSubmit() {
      this.submitted = true;
      const { username, email, password } = this.user;
      await axios ({
        method: 'post',
        url: 'http://ec2-54-183-146-26.us-west-1.compute.amazonaws.com/signup/',
        data: {
          username: username, 
          email: email, 
          password: password
        },
        headers: {'content-type': 'application/json'},
        auth: {
          username: 'admin',
          password: 'password'
        }
      })
        .then(res => console.log(res.data))
        .catch(err => console.log(err));
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
</style>
