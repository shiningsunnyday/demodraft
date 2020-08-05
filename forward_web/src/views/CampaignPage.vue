<template>
  <div>
    <h1>CampaignPage</h1>
    <CampaignRegistration />
    <CampaignDetails />
    <b-container>
      <b-form @submit.prevent="handleSubmit">
        <b-form-group
          id="address-group"
          label="Address"
          label-for="address"
        ></b-form-group>
        <b-form-input
          id="address"
          v-model="address"
          type="text"
          required
        ></b-form-input>
        <b-button type="submit">Launch</b-button>
      </b-form>
    </b-container>
    <pre>{{ civicData }}</pre>
  </div>
</template>

<script>
import CampaignRegistration from "@/components/campaign/CampaignRegistration";
import CampaignDetails from "@/components/campaign/CampaignDetails";
import * as Config from '@/config.json';

export default {
  name: "CampaignPage",
  components: {
    CampaignRegistration,
    CampaignDetails
  },
  data() {
    return {
      civicData: undefined,
      address: '',
    };
  },
  methods: {
    handleSubmit() {
      // move this to api-uils
      this.$http({
        url: `https://www.googleapis.com/civicinfo/v2/representatives`,
        method: 'GET',
        params: {
          address: this.address,
          key: Config.GOOGLE_API_KEY,
        },
      }).then(resp => {
        this.civicData = JSON.stringify(resp.data,null,'\t');
      }).catch(err => {
        alert('Please provide a valid address :-)');
        console.log(err);
      });
    }
  }
};
</script>

<style lang="scss" scoped></style>
