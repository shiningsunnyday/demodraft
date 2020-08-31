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

    <LoadingSpinner v-if="isLoading">
      "Overnight successes are generally years in the making. And most progress is made in isolation, far from the public eye." - Andrew Yang
    </LoadingSpinner>

    <PolicyList 
      v-else 
      :filteredPolicies="filteredPolicies" 
      :isFiltering="isFiltering" 
      :selectedValues="selectedValues"
      :filterPolicies="filterPolicies"
    />
  </div>
</template>

<script>
import PolicyList from '@/components/policy/PolicyList';
import Multiselect from 'vue-multiselect';
import { ApiUtil } from '@/_utils/api-utils';
import LoadingSpinner from '@/components/_common/LoadingSpinner';
import * as Config from '@/config.json';

export default {
  name: 'policies-page',
  components: {
    PolicyList,
    Multiselect,
    LoadingSpinner,
  },
  data() {
    return {
      policies: [], // holds all the policies coming from API in this component's state
      filteredPolicies: [], // holds the policies currently rendered to browser
      options: [], // holds all the values that populate the filter list
      selectedValues: [], // holds the selected filtering options the user selects
      isFiltering: false,
      isLoading: true,
    };
  },
  async created() {
    // move this to navbar.vue method
    try {
      this.policies = await ApiUtil.getPolicies();
      
      // converts policy cateogry ids into actual category names on the frontend
      // e.g. category_id 1 = "economy", category_id 2 = "education", etc. etc.
      this.policies.forEach(policy => {
        policy.categoryName = Config.policy_categories[policy.category];
        
      });
      this.filteredPolicies = this.policies;

      // Populates the Vue Multiselect list with filtering options that are linked to the incoming data
      const policyCategories = [];
      this.policies.forEach((policy) => {
        policyCategories.push(policy.categoryName);
      });

      // remove duplicate filtering options that populate the filtering lists
      this.options = [...new Set(policyCategories)];
    } catch (error) {
      alert(
        `Error ${error.response.status}: Something went wrong fetching policies`
      );
      console.error(error);
    }
    this.isLoading = false;
  },
  methods: {
    filterPolicies() {
      // If no filter options are selected, render all the policies
      // otherwise, only render policies whose 'userId' property match the currently selected filter option
      if (this.selectedValues.length === 0) {
        this.filteredPolicies = this.policies;
        this.isFiltering = false;
      } else {
        this.isFiltering = true;
        // *** I think the best way to go about filtering out the policies based on what's selected is to use "URL querying", but this will have to be built into the backend API ***
        let filteredResults = this.policies.filter(function(policy) {
          return this.indexOf(policy.categoryName) > -1;
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
    justify-content: center;
    margin: 1rem 0;
    height: 50px;
    padding-right: 10px;

    #filter {
      padding: 0;
      margin: 0 1rem;
    }

    .multiselect {
      width: 500px;
    }
  }
}
</style>
