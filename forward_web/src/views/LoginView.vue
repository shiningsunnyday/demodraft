<template>
  <div>
    <h1>Login Page</h1>

    <form>
      <label for="email">
        email
      </label>
      <input type="email">
      <label for="password">
        password
      </label>
      <input type="password">
      <button type="submit" value="Submit">Submit</button>
    </form>
  </div>
</template>

<script>
export default {
  name: "LoginView"
}
</script>

<style scoped>
form {
  display: flex;
  flex-direction: column;
  width: 300px;
  margin: 0 auto;
}
</style>