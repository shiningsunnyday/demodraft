<template>
  <div class="politician-page">
    <h1 class="politician-page__title">Browse Politicians</h1>

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
        placeholder="Filter by State"
      />
    </div>
    
    <div class="politician-page__area-container">
      <div class="politician-page__area-buttons">
        <p>Within your state: </p>
        <b-button @click="handlePoliticianArea(true)">Random</b-button>
        <b-button @click="handlePoliticianArea(false)">Ranked</b-button>
      </div>

      <div class="politician-page__area-buttons">
        <p>Country wide: </p>
        <b-button @click="handleAllPoliticians()">View All Politicians</b-button>
      </div>
    </div>
    
    <LoadingSpinner v-if="isLoading">
      "Overnight successes are generally years in the making. And most progress
      is made in isolation, far from the public eye." - Andrew Yang
    </LoadingSpinner>

    <PoliticianList v-else :filteredPoliticians="filteredPoliticians" />
  </div>
</template>

<script>
import Multiselect from 'vue-multiselect';
import PoliticianList from '@/components/politicians/PoliticianList';
import { PoliticianService } from '@/services';

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
      isLoading: true,
    };
  },
  async created() {
    this.politicians = await PoliticianService.getAllPoliticians();
    this.filteredPoliticians = this.politicians;

    // Populates a components filter list with filtering options that are linked to the incoming data
    let tempPoliticiansArr = [];
    this.politicians.forEach((politician) => {
      const loc = politician.state;
      tempPoliticiansArr.push(loc);
    });
    // remove duplicate filtering options that populate the filtering lists
    this.options = [...new Set(tempPoliticiansArr)];
    this.isLoading = false;
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
    async handlePoliticianArea(isRandom) {
      try {
        const response = await PoliticianService.getPoliticianArea(isRandom);
        this.politicians = response.data;
        this.filteredPoliticians = this.politicians;
      } catch (error) {
        alert(error);
      }
    },
    async handleAllPoliticians() {
      try {
        this.politicians = await PoliticianService.getAllPoliticians();
        this.filteredPoliticians = this.politicians;  
      } catch (error) {
        alert(error);
      }
      
    }
  },
};
</script>

<style lang="scss" scoped>
.politician-page {
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

  &__area-container{
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: start;
  }
  
  &__area-buttons {
    display: inline-flex;
    flex-direction: column;
    width: 300px;

    > * {
      margin: 4px 4px;
    }

    @media screen and (min-width: 777px) {
      flex-direction: row;
      align-items: center;
      width: 350px;
    }
  }
}
</style>
