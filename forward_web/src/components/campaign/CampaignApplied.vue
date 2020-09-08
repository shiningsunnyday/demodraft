<template>
  <div class="campaign-details">
    <LoadingSpinner v-if="isLoading" />
    <div v-else>
      <CampaignPending v-if="!isApproved" />
      <CampaignApproved v-else :politician="politician" />
    </div>
  </div>
</template>

<script>
import { ApiUtil } from '@/_utils/api-utils';
import CampaignApproved from './applied/CampaignApproved';
import CampaignPending from './applied/CampaignPending';

export default {
  name: 'CampaignApplied',
  components: {
    CampaignApproved,
    CampaignPending
  },
  data() {
    return {
      politician: {},
      isLoading: true,
    };
  },
  async created() {
    const { campaignPending } = this.$store.getters.userState;
    const user = this.$store.getters.userState;
    const modifiedPolitician = this.$store.getters.getPolitician;

    if (user.approved) {
      if (modifiedPolitician.id) {
        this.politician = modifiedPolitician;
      } else {
        await this.$store.dispatch('setPolitician', user);
        this.politician = this.$store.getters.getPolitician;
      }
      
      if (user.campaignPending) {
        await this.$store.dispatch('changeCampaignPending');
      }
    }
    
    this.isLoading = false;
  },
  computed: {
    isApproved() {
      return this.politician.approved;
    }
  }
};
</script>

<style lang="scss" scoped>
@import '@/_styles';

.campaign-details {
  @include font-sizing;
}
</style>
