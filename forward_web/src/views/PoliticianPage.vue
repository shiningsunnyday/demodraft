<template>
  <div class="politician-page">
    <div class="politician-page__filter-container">
      <p id="filter">Filter:</p>
      <Multiselect
        v-model="selectedValues"
        @input="filterPoliticians"
        :multiple="true"
        :options="options"
        :preserve-search="true"
        select-label="Click to select"
        deselect-label="Click to deselect"
        placeholder="Filter by Location"
      />
    </div>

    <PoliticianList :filteredPoliticians="filteredPoliticians" />
  </div>
</template>

<script>
import Multiselect from 'vue-multiselect';
import PoliticianList from '@/components/politicians/PoliticianList';
import { ApiUtil } from '@/_utils/api-utils';

export default {
  name: 'PoliticianPage',
  components: {
    Multiselect,
    PoliticianList,
  },
  data() {
    return {
      politicians: [], // holds the politicians data coming from API in this component's state
      filteredPoliticians: [], // holds the politicians currently rendered to browser
      options: [], // holds all the values that populate the filter list
      selectedValues: null, // holds the selected filtering options the user selects
    };
  },
  async created() {
    this.politicians = await ApiUtil.getAllPoliticians();
    this.filteredPoliticians = await this.politicians;

    // Populates a components filter list with filtering options that are linked to the incoming data
    let tempPoliticiansArr = [];
    this.politicians.forEach((politician) => {
      const loc = politician.state;
      tempPoliticiansArr.push(loc);
    });
    // remove duplicate filtering options that populate the filtering lists
    this.options = [...new Set(tempPoliticiansArr)];
  },
  methods: {
    filterPoliticians() {
      // If no filter options are selected, render all the politicians
      // otherwise, only render politicians whose 'location' property match the currently selected filter option
      if (this.selectedValues.length === 0) {
        this.filteredPoliticians = this.politicians;
      } else {
        let filteredResults = this.politicians.filter(function(politician) {
          const loc = politician.state;

          return this.indexOf(loc) > -1;
        }, this.selectedValues);

        this.filteredPoliticians = filteredResults;
      }
    },
  },
};
</script>

<style lang="scss" scoped>
.politician-page {
  text-align: center;

  &__filter-container {
    display: flex;
    align-items: center;
    margin: 1rem 0;
    height: 50px;
    
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
