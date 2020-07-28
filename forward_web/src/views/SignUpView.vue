<template>
  <div class="signup">
    <h1 class="signup__title">Sign Up</h1>
    <b-form class="signup__form" @submit.prevent="handleSubmit">
      <b-form-group id="username-group" label="Username" label-for="username">
        <b-form-input
          id="username"
          v-model="user.username"
          type="text"
          required
        ></b-form-input>
      </b-form-group>

      <b-form-group
        id="email-group"
        label="Email address:"
        label-for="email"
        description="We'll never share your email with anyone else."
      >
        <b-form-input
          id="email"
          v-model="user.email"
          type="email"
          required
        ></b-form-input>
      </b-form-group>

      <b-form-group id="password-group" label="Password" label-for="password">
        <b-form-input
          id="password"
          v-model="user.password"
          type="password"
          required
        ></b-form-input>
      </b-form-group>
      
      <div class="signup__footer">
        <b-button type="submit" variant="primary">
          Submit
        </b-button>
        <router-link to="/login" class="signup__link">
          Already have an account? Login!
        </router-link>
      </div>
    </b-form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'SignUpView',
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
    async handleSubmit(e) {
      this.submitted = true;
      const { username, email, password } = this.user;
      console.log(username);
      console.log(email);
      console.log(password);
      // await axios
      //   .post(
      //     'http://ec2-18-144-155-31.us-west-1.compute.amazonaws.com/users/',
      //     { username, email, password }
      //   )
      //   .then((res) => console.log(res.data))
      //   .catch((err) => console.log(err));
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
