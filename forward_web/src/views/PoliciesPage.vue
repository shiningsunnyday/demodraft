<template>
  <div class="policies">
    <h1 class="policies__title">Policies</h1>

    <div class="policies__filter-container">
      <p id="filter">Filter:</p>
      <Multiselect
        v-model="selectedValues"
        @input="filterPolicies"
        :multiple="true"
        :options="options"
        :close-on-select="false"
        :preserve-search="true"
        select-label="Click to select"
        deselect-label="Click to deselect"
        placeholder="Filter by Category"
      />
    </div>
    <div v-if="isLoadingPolicies">Loading...</div>
    <div v-else class="policies__policies-container">
      <!-- add isfiltered boolean -->
      <PolicyList v-bind:filteredPolicies="filteredPolicies" />
    </div>
  </div>
</template>

<script>
import PolicyList from '@/components/policy/PolicyList';
import Multiselect from 'vue-multiselect';
import { ApiUtil } from '@/_utils/api-utils';

export default {
  name: 'policies-page',
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
      isLoadingPolicies: true,
    };
  },
  async created() {
    // move this to navbar.vue method
    try {
      this.policies = await ApiUtil.getPolicies();
      this.filteredPolicies = this.policies;
      // Populates a components filter list with filtering options that are linked to the incoming data
      const policyCategories = [];
      this.policies.forEach((policy) => {
        policyCategories.push(policy.category);
      });
      // remove duplicate filtering options that populate the filtering lists
      this.options = [...new Set(policyCategories)];
    } catch (error) {
      alert(`Error ${error.response.status}: Something went wrong fetching policies`);
      console.error(error);
    }
    this.isLoadingPolicies = false;
  },
  methods: {
    filterPolicies() {
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
};
</script>

// Vue Multiselect styling
<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>

<style lang="scss" scoped>
.scroller {
  height: 100%;
}

.name {
  padding: 0 12px;
  display: flex;
  align-items: center;
}

.policies {
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
