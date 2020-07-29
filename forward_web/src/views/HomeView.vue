<template>
  <div class="home">
    <h1 class="home__title">Home</h1>

    <div class="home__policies-container">
      <Policies v-bind:policies="policies" />
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Policies from "../components/Policies";

export default {
  name: "HomeView",
  components: {
    Policies,
  },
  data() {
    return {
      policies: [],
    };
  },
  methods: {},
  created() {
    axios
      .get("https://jsonplaceholder.typicode.com/posts?_limit=10")
      .then((response) => {
        this.policies = response.data;
      })
      .catch((error) => {
        console.log(error);
      });
  },
};
</script>

<style lang="scss" scoped>
.home {
  text-align: center;

  &__picture {
    max-width: 310px;
    margin: 1em;

    @media screen and (min-width: 768px) {
      max-width: 410px;
    }
  }

  &__button {
    margin: 1em;
  }
}
</style>
