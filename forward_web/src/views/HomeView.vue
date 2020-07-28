<template>
  <div>
    <h1>HomePage</h1>

    <img
      alt="Vue logo"
      src="../assets/once_again.jpg"
      width="30%"
      height="100%"
    />
    <h1>{{ msg }}</h1>
    <button type="button" id="get-politicians" @click="fetchInit">
      Politicians
    </button>
    <ul class="politician-list" id="politician-list">
      <li v-for="p in res" :key="p.name">
        <p>{{ p.name }}</p>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: "HomeView",
  data() {
    return {
      msg: "Humanity Forward!!!",
      res: [],
      avail: false,
    };
  },
  methods: {
    fetchInit() {
      fetch(
        "http://ec2-18-144-155-31.us-west-1.compute.amazonaws.com/politicians",
        {
          method: "GET",
        }
      )
        .then((res) => {
          if (res.ok) {
            return res.json();
          }
        })
        .then((res) => {
          this.res = res;
          this.avail = true;
          console.log(res);
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
};
</script>

<style scoped></style>
