<template>
  <div class="home">
    <h1 class="home__title">Home</h1>

    <div class="home__filter-container">
      <p id="filter">Filter:</p>
      <multiselect
        v-model="values"
        @input="filterPolicies"
        :multiple="true"
        :options="options"
        select-label=""
        deselect-label=""
      />
      <p>{{ values }}</p>
    </div>

    <div class="home__policies-container">
      <Policies v-bind:policies="policies" />
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Policies from "../components/Policies";
import Multiselect from "vue-multiselect";

export default {
  name: "HomeView",
  components: {
    Policies,
    Multiselect,
  },
  data() {
    return {
      policies: [],
      options: [],
      values: null,
    };
  },
  methods: {
    removeDuplicates(arr) {
      arr.splice(0, arr.length, ...new Set(arr));
    },
    async filterPolicies() {
      // *** Figure out how to filter out policies based on an ARRAY of (aka, multiple) filter options ***
      console.log(this.values.length);

      // If no filter options are selected, render all the policies
      // otherwise, only render policies whose 'userId' property match the currently selected filter option
      if (this.values.length === 0) {
        await axios
          .get("https://jsonplaceholder.typicode.com/posts?_limit=100")
          .then((response) => {
            this.policies = response.data;
          })
          .catch((error) => {
            console.log(error);
          });
      } else {
        await axios
          .get(
            `https://jsonplaceholder.typicode.com/posts/?userId=${this.values[0]}`
          )
          .then((response) => (this.policies = response.data))
          .catch((error) => console.log(error));
      }
    },
  },
  async created() {
    await axios
      .get("https://jsonplaceholder.typicode.com/posts?_limit=100")
      .then((response) => {
        this.policies = response.data;
      })
      .catch((error) => {
        console.log(error);
      });

    // *** May need to refactor code for better speed, efficiency, etc. ***
    // When the HomeView component is mounted, populate the filter list with options after the axios call is made since the options are linked to the incoming data
    // At the moment, since dummy data is being used, the removeDuplicates() method removes duplicate filtering options
    await this.policies.forEach((policy) => this.options.push(policy.userId));
    this.removeDuplicates(this.options);
  },
};
</script>

// Vue Multiselect styling
<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>

<style lang="scss" scoped>
.home {
  text-align: center;

  &__filter-container {
    display: flex;
    align-items: center;

    #filter {
      padding: 0;
      margin: 0 15px;
    }

    .multiselect {
      width: 500px;
    }
  }
}
</style>
