<template>
  <b-container>
    <CampaignRegistration v-if="!isCampaignLaunched" @handle-campaign-launch="handleCampaignLaunch"/>
    <CampaignDetails v-if="isCampaignLaunched" />
  </b-container>
</template>

<script>
import CampaignRegistration from '@/components/campaign/CampaignRegistration';
import CampaignDetails from '@/components/campaign/CampaignDetails';
import * as Config from '@/config.json';
import { ApiUtil } from '../_utils/api-utils';

export default {
  name: 'CampaignPage',
  components: {
    CampaignRegistration,
    CampaignDetails,
  },
  data() {
    return {
      isCampaignLaunched: false,
    };
  },
  created() {
    const currentUser = this.$store.getters.getUserInfo;
    if (
      typeof currentUser.approved !== 'undefined' ||
      currentUser.campaignPending
    ) {
      this.isCampaignLaunched = true;
    }
  },
  methods: {
    handleCampaignLaunch(event) {
      this.isCampaignLaunched = event;
    },
  },
};
</script>

<style lang="scss" scoped>
h1 {
  color: red;
  text-align: center;
  margin-bottom: 3rem;
}
.center {
  display: flex;
  justify-content: center;
}
</style>
