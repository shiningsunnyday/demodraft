<template>
  <div class="home">
    <h1 class="home__title">Home</h1>

    <img class="home__picture" src="../assets/once_again.jpg" />
    <h2>{{ msg }}</h2>
    <b-button
      type="button"
      id="get-politicians"
      class="home__button"
      @click="fetchInit"
    >
      Politicians
    </b-button>
    <ul class="home__politician-list" id="politician-list">
      <li v-for="p in politicians" :key="p.name">
        <p>{{ p.name }}</p>
      </li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  name: 'HomeView',
  data() {
    return {
      msg: 'Humanity Forward!!!',
      politicians: [],
      avail: false,
    };
  },
  methods: {
    fetchInit() {
      axios
        .get(
          'http://ec2-18-144-155-31.us-west-1.compute.amazonaws.com/politicians'
        )
        .then((response) => {
          this.politicians = response.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
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

  &__politician-list {
    list-style: none;
    padding: 0;
  }
}
</style>
