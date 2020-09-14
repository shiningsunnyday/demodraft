<template>
  <div class="campaign-details">
    <CampaignPending v-if="!isApproved" />
    <CampaignApproved v-else />
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
    CampaignPending,
  },
  data() {
    return {};
  },
  computed: {
    isApproved() {
      return this.$store.getters.userState.approved;
    },
  },
};
</script>

<style lang="scss" scoped>
@import '@/_styles';

.campaign-details {
  @include font-sizing;
}
</style>
