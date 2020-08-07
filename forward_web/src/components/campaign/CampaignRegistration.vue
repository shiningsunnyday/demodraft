<template>
  <div>
    <CampaignAddressSearch :address="address" @handle-submit="handleSubmit" />

    <b-form @submit.prevent="handleSubmitCampaign">
      <b-container>
        <b-form-group label="City/County Positions">
          <b-form-radio-group
            stacked
            v-model="selectedPos"
            v-for="(position, index) in cityPos"
            :key="index"
          >
            <b-form-radio
              :value="{ name: position.name, index: index, scope: 'local' }"
            >
              {{ position.name }}
            </b-form-radio>
          </b-form-radio-group>
        </b-form-group>

        <b-form-group label="State Positions">
          <b-form-radio-group
            stacked
            v-model="selectedPos"
            v-for="(position, index) in statePos"
            :key="index"
          >
            <b-form-radio
              :value="{ name: position.name, index: index, scope: 'state' }"
            >
              {{ position.name }}
            </b-form-radio>
          </b-form-radio-group>
        </b-form-group>

        <b-form-group label="Federal Positions">
          <b-form-radio-group
            stacked
            v-model="selectedPos"
            v-for="(position, index) in federalPos"
            :key="index"
          >
            <b-form-radio
              :value="{ name: position.name, index: index, scope: 'federal' }"
            >
              {{ position.name }}
            </b-form-radio>
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
import * as Config from '@/config.json';
import { ApiUtil } from '@/_utils/api-utils';

export default {
  name: 'CampaignRegistration',
  components: {
    CampaignAddressSearch
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
      const data = { address: event}; // converting string to object for API purposes
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

      console.log(response);
    },
  },
};
</script>

<style lang="scss" scoped></style>
