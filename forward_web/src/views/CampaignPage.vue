<template>
  <div>
    <h1>CampaignPage</h1>
    <CampaignRegistration />
    <CampaignDetails />
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
};
</script>

<style lang="scss" scoped></style>
