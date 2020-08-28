<template>
  <div>
    <b-container class="campaign-reg__description">
      Search for representative positions at every level of government that
      represents your address. Then select a position you would like to launch
      your campaign for.
    </b-container>

    <CampaignAddressSearch
      @handleSearch="handleSearch"
      :isSearching="isSearching"
    />

    <hr />

    <b-container>
      <b-form @submit.prevent="handleSubmitCampaign">
        <CampaignFormGroup
          :positions="positions"
          @update-selected-pos="updateSelectedPos"
        />

        <b-button class="launch-button" v-if="isLaunching" disabled>
          <b-spinner small type="grow"></b-spinner>
          Launching...
        </b-button>

        <b-button
          v-else-if="civicData.local"
          class="launch-button"
          type="submit"
        >
          Launch
        </b-button>
      </b-form>
    </b-container>
  </div>
</template>

<script>
import CampaignAddressSearch from './CampaignAddressSearch';
import CampaignFormGroup from './CampaignFormGroup';
import { ApiUtil } from '@/_utils/api-utils';
import { simulateApiCall } from '@/_utils/common-utils.js';

export default {
  name: 'CampaignRegistration',
  components: {
    CampaignAddressSearch,
    CampaignFormGroup,
  },
  data() {
    return {
      civicData: {},
      positions: {},
      selectedPos: {},
      isLaunching: false,
      isSearching: false,
    };
  },
  methods: {
    async handleSearch(address) {
      try {
        this.isSearching = true;
        this.civicData = await ApiUtil.postAddress({
          username: this.$store.getters.username,
          password: this.$store.getters.password,
          address: address,
        });
        this.positions = {
          local: this.civicData.local,
          state: this.civicData.state,
          country: this.civicData.country,
        };
      } catch (error) {
        alert(`Oops, we couldn't find positions for that address. Make sure it's in the correct format!`);
      }
      this.isSearching = false;
    },
    async handleSubmitCampaign() {
      const { username, campaignPending } = this.$store.getters.getUserInfo;
      const data = {
        username: username,
        scope: this.selectedPos.scope,
        index: this.selectedPos.index,
      };

      if (data.scope) {
        try {
          this.isLaunching = true;
          //await simulateApiCall();
          const response = await ApiUtil.submitCampaign(data);
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
        } catch (error) {
          alert(`Oops, something went wrong.`);
        }
        this.isLaunching = false;
        // change to campaign details view
        this.$emit('handle-campaign-launch', true);
        return;
      }

      return alert('Choose a position for your campaign!');
    },
    updateSelectedPos(event) {
      this.selectedPos = event;
    },
  },
};
</script>

<style lang="scss" scoped>
.campaign-reg {
  &__description {
    max-width: 550px;
    margin-bottom: 3rem;
  }
}
.launch-button {
  margin-bottom: 5rem;
}
</style>
