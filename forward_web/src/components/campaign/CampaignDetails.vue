<template>
  <div class="campaign-details">
    <LoadingSpinner v-if="isLoading"></LoadingSpinner>

    <div v-else>
      <div class="campaign-details__pending-status" v-if="!isApproved">
        <h4>
          Thank you for submitting a request to launch your campaign!
        </h4>
        <!-- <br /> -->
        <h4>You will be notified when your application is accepted.</h4>
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
      // username,
      // password,
      campaignPending,
    } = this.$store.getters.userState;

    // re-logs in to update campaign status (don't know if want)
    // await this.$store.dispatch('login', {
    //   username,
    //   password,
    //   campaignPending,
    // });

    const user = this.$store.getters.userState;
    const modifiedPolitician = this.$store.getters.getPolitician;

    if (user.approved) {
      if (modifiedPolitician.id) {
        this.politician = modifiedPolitician;
      } else {
        await this.$store.dispatch('setPolitician', user);
        this.politician = this.$store.getters.getPolitician;
      }

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
    margin-top: 100px;
    text-align: center;

    h4 {
      margin-bottom: 20px;
    }
  }
}
</style>
