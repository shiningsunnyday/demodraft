<template>
  <b-container>
    <h1>Campaign Page</h1>
    <div class="center">
      <CampaignRegistration v-if="!isCampaignLaunched" />
      <CampaignDetails v-if="isCampaignLaunched" />
    </div>
  </b-container>
</template>

<script>
import CampaignRegistration from '@/components/campaign/CampaignRegistration';
import CampaignDetails from '@/components/campaign/CampaignDetails';
import * as Config from '@/config.json';

export default {
  name: 'CampaignPage',
  components: {
    CampaignRegistration,
    CampaignDetails,
  },
  computed: {
    isCampaignLaunched() {
      const currentUser = this.$store.getters.getUserInfo;

      // campaign never launched
      if (typeof currentUser.approved === 'undefined') {
        return false;
      }

      // campaign launched
      if (!currentUser.approved || currentUser.approved) {
        return true;
      }
    },
  },
  methods: {},
};
</script>

<style lang="scss" scoped>
h1 {
  color: red;
  text-align: center;
  margin-bottom: 5rem;
}
.center {
  display: flex;
  justify-content: center;
}
</style>
