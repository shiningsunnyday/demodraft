<template>
  <div>
    <CampaignAddressSearch @handle-submit="handleSubmit" />
    <hr />
    <b-form @submit.prevent="handleSubmitCampaign">
      <b-container>
        <CampaignFormGroup
          :positions="positions"
          @update-selected-pos="updateSelectedPos"
        />
        <b-button v-if="isLoading" disabled>
          <b-spinner small></b-spinner>
          <span class="sr-only">Loading...</span>
        </b-button>
        <b-button v-else class="launch-button" type="submit">Launch</b-button>
      </b-container>
    </b-form>
  </div>
</template>

<script>
import CampaignAddressSearch from './CampaignAddressSearch';
import CampaignFormGroup from './CampaignFormGroup';
import * as Config from '@/config.json';
import { ApiUtil } from '@/_utils/api-utils';

export default {
  name: 'CampaignRegistration',
  components: {
    CampaignAddressSearch,
    CampaignFormGroup,
  },
  data() {
    return {
      civicData: {},
      address: '',
      status: null,
      positions: {},
      selectedPos: {},
      successModal: '',
      isLoading: false,
    };
  },
  methods: {
    async handleSubmit(event) {
      try {
        const response = await ApiUtil.postAddress({
          username: this.$store.getters.username,
          password: this.$store.getters.password, // security risk, will need to use session cookies/JWT
          address: event,
        });
        this.civicData = response.data;
        this.positions = {
          local: this.civicData.local,
          state: this.civicData.state,
          country: this.civicData.country,
        };
      } catch (error) {
        console.log(error.message);
      }
    },
    async handleSubmitCampaign() {
      const { username, campaignPending } = this.$store.getters.getUserInfo;
      const data = {
        username: username,
        scope: this.selectedPos.scope,
        index: this.selectedPos.index,
      };

      if (data.scope) {
        this.isLoading = true;
        const response = await ApiUtil.submitCampaign(data);
        // console.log(response);
        this.successModal = '';
        const modalMessage = `Campaign successfully submited!`;
        await this.$bvModal.msgBoxOk(modalMessage, {
          title: 'Confirmation',
          size: 'sm',
          buttonSize: 'sm',
          okVariant: 'success',
          headerClass: 'p-2 border-bottom-0',
          footerClass: 'p-2 border-top-0',
          centered: true,
        });
        this.$store.dispatch('changeCampaignPending');
        this.isLoading = false;
        this.$emit('handle-campaign-launch', true);
      } else {
        alert('Choose a position for your campaign!');
      }
    },
    updateSelectedPos(event) {
      this.selectedPos = event;
    },
  },
};
</script>

<style lang="scss" scoped>
.launch-button {
  margin-bottom: 5rem;
}
</style>
