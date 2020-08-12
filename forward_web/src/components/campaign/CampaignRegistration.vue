<template>
  <div>
    <CampaignAddressSearch @handle-submit="handleSubmit" />
    <hr />
    <b-form @submit.prevent="handleSubmitCampaign">
      <b-container>
        <CampaignFormGroup
          :positions="positions"
          @update-selected-pos="updateSelectedPos"
        />
        <b-button class="launch-button" type="submit">Launch</b-button>
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
  created() {
    console.log(this.$store.getters.getUserInfo);
  },
  methods: {
    async handleSubmit(event) {
      try {
        const response = await ApiUtil.postAddress({
          username: this.$store.getters.username,
          password: this.$store.getters.password, // security risk, will need to use session cookies/JWT
          address: event,
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
    getUniquePositions(position) {
      const set = new Set();
      const result = [];
      position.forEach((positionObject) => {
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
        /** This works now **/ 
        // const response = await ApiUtil.submitCampaign(data);
        // console.log(response);
        /** This works now **/ 

        // TODO
        // loading spinner on Launch button (before calling await ApiUtil.submitCampaign(data))
        // success modal

        /**
         * Vuex
         * 1. grab the politician id from response.data.id and axios call GET campaign/?politician_id=response.data.id
         * OR
         * 2. set/create approved = false in user store
         * finally, change current view to pending Campaign Details & navbar from Launch Campaign >> My Campaign
         */
        alert(
          `${data.username} applied for ${this.selectedPos.name}\nusername: ${data.username}\nscope: ${data.scope}\nindex: ${data.index}`
        );
        console.log(data);
      } else {
        alert('Choose a position for your campaign!');
      }
    },
    updateSelectedPos(event) {
      this.selectedPos = event;
    },
  },
};
</script>

<style lang="scss" scoped>
.launch-button {
  margin-bottom: 5rem;
}
</style>
