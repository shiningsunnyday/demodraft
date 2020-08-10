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
      <hr />
      <ul>
        <li>Position Applied For</li>
        <li>Fundraise Goal</li>
        <li>Funds Raised</li>
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
      fakeApproved: false,
    };
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
