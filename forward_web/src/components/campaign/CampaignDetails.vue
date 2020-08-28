<template>
  <div class="campaign-details">
    <LoadingSpinner v-if="isLoading"></LoadingSpinner>

    <div class="campaign-details__pending-status" v-if="!isApproved">
      <p>
        Thank you for submitting a request to launch your campaign!
        <br>
        You will be notified when your application is accepted.
      </p>
    </div>

    <CampaignApproved v-else :politician="politician" />
  </div>
</template>

<script>
import { ApiUtil } from '@/_utils/api-utils';
import { simulateApiCall } from '@/_utils/common-utils';
import CampaignApproved from './CampaignApproved';
import LoadingSpinner from '@/components/_common/LoadingSpinner';

export default {
  name: 'CampaignDetails',
  components: {
    CampaignApproved,
    LoadingSpinner,
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
@import '@/_styles';

.campaign-details {
  @include font-sizing;

  &__pending-status {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }
}
</style>
