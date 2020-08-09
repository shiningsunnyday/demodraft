<template>
  <div>
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
      try {
        const response = await ApiUtil.postAddress({ 
          username: this.$store.getters.username,
          password: this.$store.getters.password, // security risk, will need to use session cookies/JWT
          address: event 
        });
        this.civicData = response.data;
        this.positions = {
          local: this.civicData.local,
          state: this.civicData.state,
          country: this.civicData.country,
        }; 
      } catch (error) {
        console.log(error.message);
      }
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

      if (data.scope) {
        const response = await ApiUtil.submitCampaign(data);

        this.$store.dispatch('changeCampaignStatus');
        console.log(response);
      } else {
        alert('Choose a position for your campaign!');
      }
      
    },
    updateSelectedPos(event) {
      this.selectedPos = event;
    },
  },
  created() {
    console.log(this.$store.getters.getUserInfo);
  }
};
</script>

<style lang="scss" scoped></style>
