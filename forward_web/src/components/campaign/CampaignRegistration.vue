<template>
  <div>
    <b-container class="campaign-reg__description">
      {{ description }}
    </b-container>
    <hr />
    <div class="campaign-reg__steps">
      <CampaignAddressSearch
        v-show="campaignProgress === 0"
        @handleSearch="handleSearch"
        :isSearching="isSearching"
      />

      <CampaignPositions
        v-show="campaignProgress === 1"
        @handleBack="$emit('pushStepOne')"
        @handlePositionSelected="handlePositionSelected"
        :positions="positions"
      />

      <CampaignInformation 
        v-show="campaignProgress === 2"
        @handleBack="$emit('pushStepTwo')"
        @handleSubmitCampaign="handleSubmitCampaign"
        :data="selectedPosition"
        :isLaunching="isLaunching"
      />
    </div>
  </div>
</template>

<script>
import CampaignAddressSearch from './CampaignAddressSearch';
import CampaignPositions from './CampaignPositions';
import CampaignInformation from './CampaignInformation';
import { ApiUtil } from '@/_utils/api-utils';
import { simulateApiCall } from '@/_utils/common-utils.js';

export default {
  name: 'CampaignRegistration',
  components: {
    CampaignAddressSearch,
    CampaignPositions,
    CampaignInformation
  },
  props: {
    campaignProgress: Number,
  },
  data() {
    return {
      civicData: {},
      positions: {},
      selectedPosition: {},
      isLaunching: false,
      isSearching: false,
    };
  },
  computed: {
    description() {
      if (this.campaignProgress === 0) {
        return `Planning to run for office and ready to launch a campaign on Demodraft? Lets start by searching for representative positions at every level of government that represents your address.`;
      }

      if (this.campaignProgress === 1) {
        return 'Here are the available offices we found that you can run your campaign in. Select a position you would like to launch your campaign for.';
      }

      const position = this.selectedPosition.name;
      if (position) {
        return `Whenever you're ready, click the large blue button to launch your campaign for ${position}!`;
      }
    }
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
        this.$emit('pushStepTwo');
      } catch (error) {
        alert(`Oops, we couldn't find positions for that address. Make sure it's in the correct format!`);
      }
      this.isSearching = false;
    },
    handlePositionSelected(selectedPosition) {
      this.selectedPosition = selectedPosition;
      this.$emit('pushStepThree');
    },
    async handleSubmitCampaign() {
      const { username, campaignPending } = this.$store.getters.getUserInfo;
      const data = {
        username: username,
        scope: this.selectedPosition.scope,
        index: this.selectedPosition.index,
      };

      if (data.scope) {
        try {
          this.isLaunching = true;
          // await simulateApiCall();
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
        return this.$emit('completeAllSteps', true);
      }
      return alert('Choose a position for your campaign!');
    },
  },
};
</script>

<style lang="scss" scoped>
.campaign-reg {
  &__description {
    max-width: 700px;
    padding: 1em;
    text-align: center;
    font-weight: bold;
  }

  &__steps {
    display: flex;
    justify-content: center;
    padding: 1em 0 2em 0;
  }
}
</style>
