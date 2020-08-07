<template>
  <div>
    <CampaignAddressSearch :address="address" @handle-submit="handleSubmit" />

    <b-form @submit.prevent="handleSubmitCampaign">
      <b-container>
        <b-form-group>
          <b-form-radio-group stacked>
            <h4>City/County Positions</h4>
            <CampaignFormGroup
              label="City/County Positions"
              :selectedPos="selectedPos"
              :positions="cityPos"
              @update-selected-pos="updateSelectedPos"
            />

            <h4>State Positions</h4>
            <CampaignFormGroup
              label="State Positions"
              :selectedPos="selectedPos"
              :positions="statePos"
              @update-selected-pos="updateSelectedPos"
            />

            <h4>Federal Positions</h4>
            <CampaignFormGroup
              label="Federal Positions"
              :selectedPos="selectedPos"
              :positions="federalPos"
              @update-selected-pos="updateSelectedPos"
            />
          </b-form-radio-group>
        </b-form-group>

        <b-button type="submit">Launch</b-button>
      </b-container>
    </b-form>

    <div>{{ selectedPos }}</div>
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
      civicData: undefined,
      address: '',
      status: null,
      cityPos: [],
      statePos: [],
      federalPos: [],
      selectedPos: {},
    };
  },
  methods: {
    async handleSubmit(event) {
      // POST /address/
      // example request: {"address":"1263 Pacific Ave. Kansas City, KS"}
      this.address = event; // update state
      const data = { address: event }; // converting string to object for API purposes
      this.civicData = await ApiUtil.postAddress(data);
      this.statePos = [...new Set(this.civicData.data.administrativeArea1)];
      this.federalPos = [...new Set(this.civicData.data.country)];

      // *** May have to refactor or remove this originalCityArr related code later ***
      // The API call will sometimes return duplicates of the same position titles, but with differnt division ids
      // this forEach code prevents duplicate positions from being rendered in the list of selectable positions in the browser
      const originalCityArr = this.civicData.data.administrativeArea2;
      let tempSet = new Set();
      originalCityArr.forEach((currObj) => {
        if (!tempSet.has(currObj.name)) {
          tempSet.add(currObj.name);
          this.cityPos.push(currObj);
        }
      });
    },

    async handleSubmitCampaign() {
      let response = await ApiUtil.submitCampaign({
        username: this.$store.getters.username,
        scope: this.selectedPos.scope,
        index: this.selectedPos.index,
      });
    },

    updateSelectedPos(event) {
      this.selectedPos = event;
    },
  },
};
</script>

<style lang="scss" scoped></style>
