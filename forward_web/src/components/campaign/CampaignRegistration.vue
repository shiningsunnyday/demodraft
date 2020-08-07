<template>
  <div>
    <div>{{ selectedPos }}</div>
    <CampaignAddressSearch @handle-submit="handleSubmit" />
    <hr>
    <b-form @submit.prevent="handleSubmitCampaign">
      <b-container>
        <CampaignFormGroup
          :positions="positions"
          @update-selected-pos="updateSelectedPos"
        />
        <b-button type="submit">Launch</b-button>
      </b-container>
    </b-form>
  </div>
</template>

<script>
import CampaignAddressSearch from './CampaignAddressSearch';
import CampaignFormGroup from './CampaignFormGroup';
import * as Config from '@/config.json';
import { ApiUtil } from '@/_utils/api-utils';

export default {
  name: 'CampaignRegistration',
  components: {
    CampaignAddressSearch,
    CampaignFormGroup,
  },
  data() {
    return {
      civicData: {},
      address: '',
      status: null,
      positions: {},
      selectedPos: {},
    };
  },
  methods: {
    async handleSubmit(event) {
      // POST /address/
      // example request: {"address":"1263 Pacific Ave. Kansas City, KS"}
      const response = await ApiUtil.postAddress({ address: event });
      this.civicData = response.data;
      this.positions = {
        local: this.getUniquePositions(this.civicData.administrativeArea2),
        state: this.getUniquePositions(this.civicData.administrativeArea1),
        federal: this.getUniquePositions(this.civicData.country),
      };
    },
    // *** May have to refactor or remove this method later ***
    // The API call will sometimes return duplicates of the same position titles, but with unique division ids.
    // This method prevents duplicate positions names from being rendered in the selectable list
    getUniquePositions(position) { 
      const set = new Set();
      const result = [];
      position.forEach(positionObject => {
        if (!set.has(positionObject.name)) {
          set.add(positionObject.name);
          result.push(positionObject);
        }
      });

      return result;
    },
    async handleSubmitCampaign() {
      const data = {
        username: this.$store.getters.username,
        scope: this.selectedPos.scope,
        index: this.selectedPos.index,  
      };

      //let response = await ApiUtil.submitCampaign(data);
      console.log(data);
    },
    updateSelectedPos(event) {
      this.selectedPos = event;
    },
  },
};
</script>

<style lang="scss" scoped></style>
