<template>
  <div>
    <h1>CampaignDetails</h1>
    <div v-if="!isApproved">
      <h1>Thank you for submitting your campaign! 😄</h1>
      <h3>
        Your current submission is: Pending
      </h3>
      <h4>We'll notify you when your submission status is updated</h4>
    </div>

    <div v-if="isApproved">
      <h1>Your Campaign Info</h1>
      <h2>Running for: {{ campaign.name }}</h2>
      <hr />
      <ul>
        <li>ActBlue: {{ campaign.actblue }}</li>
        <li>Fundraise Goal: {{ campaign.fundraise_goal }}</li>
        <li>Funds Raised: {{ campaign.fundraised }}</li>
      </ul>
    </div>
  </div>
</template>

<script>
import { ApiUtil } from '@/_utils/api-utils';

export default {
  name: 'CampaignDetails',
  data() {
    return {
      user: {},
      campaign: {},
      fakeApproved: false,
    };
  },
  async created() {
    const currentUser = this.$store.getters.getUserInfo;
    if (currentUser.approved) {
      this.campaign = await ApiUtil.getCampaign(currentUser.politician_id);
    }

  },
  computed: {
    isApproved() {
      const currentUser = this.$store.getters.getUserInfo;

      // campaign never launched
      // redundant guard clause for now
      if (typeof currentUser.approved === 'undefined') {
        return false;
      }

      return currentUser.approved;
    },
  },
  methods: {},
};
</script>

<style lang="scss" scoped></style>
