<template>
  <div>
    <h1>CampaignPage</h1>
    <CampaignRegistration v-if="!getCampaignStatus" />
    <!-- ?? <SelectPositionComponent /> ?? 
    After clicking the Launch button in the <CampaignRegistration /> component, send the data returned from the Google API call into this component where the user will be able to select the position(s?) they're interested in?
    -->
    <CampaignDetails v-if="getCampaignStatus" />
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
    getCampaignStatus() {
      return this.$store.getters.userCampaignStatus;
    }
  }
};
</script>

<style lang="scss" scoped></style>
