<template>
  <div>
    <h1>CampaignPage</h1>
    <b-button @click="toggleLaunchCampaign">Toggle Launch Campaign</b-button>
    <CampaignRegistration v-if="!isCampaignLaunched" />
    <!-- ?? <SelectPositionComponent /> ?? 
    After clicking the Launch button in the <CampaignRegistration /> component, send the data returned from the Google API call into this component where the user will be able to select the position(s?) they're interested in?
    -->
    <CampaignDetails v-if="isCampaignLaunched" />
  </div>
</template>

<script>
import CampaignRegistration from "@/components/campaign/CampaignRegistration";
import CampaignDetails from "@/components/campaign/CampaignDetails";
import * as Config from "@/config.json";

export default {
  name: "CampaignPage",
  components: {
    CampaignRegistration,
    CampaignDetails,
  },
  computed: {
    isCampaignLaunched() {
      return this.$store.getters.userCampaignStatus;
    }
  },
  methods: {
    // for testing purposes
    toggleLaunchCampaign() {
      this.$store.dispatch('changeCampaignStatus');
    },
  }
};
</script>

<style lang="scss" scoped></style>
