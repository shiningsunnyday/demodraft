<template>
  <div>
    <h1>CampaignDetails</h1>
    <b-button @click="toggleSubmissionStatus">Toggle Submission Status</b-button>

    <b-container v-if="!fakeApproved">
      <h1>Thank you for submitting your campaign! 😄</h1>
      <h3>
        Your current submission is: Pending
      </h3>
      <h4>We'll notify you when your submission status is updated</h4>
    </b-container>

    <b-container v-if="fakeApproved">
      <h1>Your Campaign Info</h1>
      <hr />
      <ul>
        <li>Position Applied For</li>
        <li>Fundraise Goal</li>
        <li>Funds Raised</li>
      </ul>
    </b-container>
  </div>
</template>

<script>
import { ApiUtil } from '@/_utils/api-utils';

export default {
  name: 'CampaignDetails',
  data() {
    return {
      user: {},
      fakeApproved: false,
    };
  },
  methods: {
    toggleSubmissionStatus() {
      this.fakeApproved = !this.fakeApproved;
    }
  },
  // created() {
  //   const { politician_id } = this.$store.getters.getUserInfo;
  //   ApiUtil.getCampaign(politician_id);
  // },
};
</script>

<style lang="scss" scoped></style>
