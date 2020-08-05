<template>
  <div class="home">
    <h1 class="home__title">Home</h1>

    <div class="home__filter-container">
      <p id="filter">Filter:</p>
      <Multiselect
        v-model="selectedValues"
        @input="filterPolicies"
        :multiple="true"
        :options="options"
        :close-on-select="false"
        :preserve-search="true"
        select-label=""
        deselect-label=""
        placeholder="Filter by Category"
      />
    </div>

    <div class="home__policies-container">
      <PolicyList v-bind:filteredPolicies="filteredPolicies" />
    </div>
  </div>
</template>

<script>
import PolicyList from "../components/PolicyList";
import Multiselect from "vue-multiselect";
import { ApiUtil } from "../_utils/api-utils";

export default {
  name: "home-page",
  components: {
    PolicyList,
    Multiselect,
  },
  data() {
    return {
      policies: [], // holds all the policies coming from API in this component's state
      filteredPolicies: [], // holds the policies currently rendered to browser
      options: [], // holds all the values that populate the filter list
      selectedValues: null, // holds the selected filtering options the user selects
    };
  },
  methods: {
    removeDuplicates(arr) {
      arr.splice(0, arr.length, ...new Set(arr));
    },
    async filterPolicies() {
      // If no filter options are selected, render all the policies
      // otherwise, only render policies whose 'userId' property match the currently selected filter option

      if (this.selectedValues.length === 0) {
        this.filteredPolicies = this.policies;
      } else {
        // *** I think the best way to go about filtering out the policies based on what's selected is to use "URL querying", but this will have to be built into the backend API ***

        let filteredResults = this.policies.filter(function(policy) {
          return this.indexOf(policy.category) > -1;
        }, this.selectedValues);

        this.filteredPolicies = filteredResults;
      }
    },
  },
  async created() {
    this.policies = await ApiUtil.getPolicies();

    this.filteredPolicies = this.policies;

    // *** May need to refactor code for better speed, efficiency, etc. ***
    // When the HomePage component is mounted, populate the filter list with options after the above axios call is made since the filtering options are linked to the incoming data
    // At the moment, since dummy data is being used, the removeDuplicates() method removes duplicate filtering options
    await this.policies.forEach((policy) => this.options.push(policy.category));
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
