<template>
  <div class="politician-page">
    <h1>PoliticianPage</h1>

    <div class="politician-page__filter-container">
      <p id="filter">Filter:</p>
      <Multiselect
        v-model="selectedValues"
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
import Multiselect from "vue-multiselect";
import PoliticianList from "../components/politicians/PoliticianList";
import { ApiUtil } from "../_utils/api-utils";

export default {
  name: "PoliticianPage",
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
    this.politicians = await ApiUtil.getPoliticians();
    this.filteredPoliticians = this.politicians;
  }
};
</script>

<style lang="scss" scoped>
.politician-page {
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
