<template>
  <b-container>
    <h1 v-if="!isCampaignLaunched">Register Campaign</h1>
    <CampaignProgressBar 
      v-if="!isCampaignLaunched"
      :currentStep="currentStep" 
    />

    <CampaignRegistration 
      v-if="!isCampaignLaunched" 
      @pushStepOne="pushStepOne"
      @pushStepTwo="pushStepTwo"
      @pushStepThree="pushStepThree"
      @completeAllSteps="completeAllSteps"
      :campaignProgress="campaignProgress"
    />

    <CampaignDetails v-if="isCampaignLaunched" />
  </b-container>
</template>

<script>
import CampaignRegistration from '@/components/campaign/CampaignRegistration';
import CampaignDetails from '@/components/campaign/CampaignDetails';
import CampaignProgressBar from '@/components/campaign/CampaignProgressBar';
import * as Config from '@/config.json';
import { ApiUtil } from '../_utils/api-utils';

export default {
  name: 'CampaignPage',
  components: {
    CampaignRegistration,
    CampaignDetails,
    CampaignProgressBar
  },
  data() {
    return {
      isCampaignLaunched: false,
      campaignProgress: 0,
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
  computed: {
    currentStep() {
      return this.campaignProgress;
    }
  },
  methods: {
    pushStepOne() {
      this.campaignProgress = 0;
    },
    pushStepTwo() {
      this.campaignProgress = 1;
    },
    pushStepThree() {
      this.campaignProgress = 2;
    },
    completeAllSteps(event) {
      this.isCampaignLaunched = event;
    },
  },
};
</script>

<style lang="scss" scoped>
h1 {
  text-align: center;
  margin-bottom: 3rem;
}
.center {
  display: flex;
  justify-content: center;
}
</style>
