<template>
  <div>
    <h1>Sign Up</h1>

    <form>
      <label for="username">
        username
      </label>
      <input type="text" name="username" v-model="username" autocomplete="off" />

      <label for="email">
        email
      </label>
      <input type="email" name="email" v-model="email" autocomplete="off" />

      <label for="password">
        password
      </label>
      <input type="password" name="password" v-model="password" autocomplete="off" />

      <button type="submit" value="Submit" @click="createNewUser(username, email, password)">Submit</button>
    </form>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "SignUpView",
  data() {
    return {
      username: "",
      email: "",
      password: "",
    };
  },
  methods: {
    async createNewUser(username, email, password) {
      event.preventDefault();

      await axios.post(
        "http://ec2-18-144-155-31.us-west-1.compute.amazonaws.com/users/",
        { username, email, password }
      )
        .then(res => console.log(res.data))
        .catch(err => console.log(err));
    },
  },
};
</script>

<style scoped>
form {
  display: flex;
  flex-direction: column;
  width: 300px;
  margin: 0 auto;
}
</style>
