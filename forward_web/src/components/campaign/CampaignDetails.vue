<template>
  <div class="campaign-details">
    <div v-if="isLoading">
      <b-spinner :variant="'secondary'" label="Loading..."></b-spinner>
    </div>
    <div v-else class="campaign-details__content">
      <div v-if="!isApproved">
        <h1>Thank you for submitting your campaign! 😄</h1>
        <h3>
          Your current submission is: Pending
        </h3>
        <h4>We'll notify you when your submission status is updated</h4>
      </div>
      <CampaignApproved v-else :politician="politician" />
    </div>
  </div>
</template>

<script>
import { ApiUtil } from '@/_utils/api-utils';
import { simulateApiCall } from '@/_utils/common-utils';
import CampaignApproved from './CampaignApproved';

export default {
  name: 'CampaignDetails',
  components: {
    CampaignApproved,
  },
  data() {
    return {
      politician: {},
      isApproved: false,
      isLoading: true,
      isUpdated: true,
      isSuccess: false,
    };
  },
  async created() {
    const {
      username,
      password,
      campaignPending,
    } = this.$store.getters.getUserInfo;
    
    await this.$store.dispatch('login', {
      username,
      password,
      campaignPending,
    });

    const user = this.$store.getters.getUserInfo;

    if (user.approved) {
      this.politician = await ApiUtil.getModifiedPolitician({ user });
      this.isApproved = this.politician.approved;

      if (user.campaignPending) {
        this.$store.dispatch('changeCampaignPending');
      }
    }

    this.isLoading = false;
  },
};
</script>

<style lang="scss" scoped>
.campaign-details {
  font-size: 14px;

  @media screen and (min-width: 768px) {
    font-size: 1rem;
  }
}
</style>
