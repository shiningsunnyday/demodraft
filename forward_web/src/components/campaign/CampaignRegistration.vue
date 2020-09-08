<template>
  <div>
    <b-container class="campaign-reg__description">
      <p>{{ description.first }}</p>
      <p>{{ description.second }}</p>
      <p>{{ description.third }}</p>
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
import CampaignAddressSearch from './registration/CampaignAddressSearch';
import CampaignPositions from './registration/CampaignPositions';
import CampaignInformation from './registration/CampaignInformation';
import { ApiUtil } from '@/_utils/api-utils';
import { simulateApiCall } from '@/_utils/common-utils.js';

export default {
  name: 'CampaignRegistration',
  components: {
    CampaignAddressSearch,
    CampaignPositions,
    CampaignInformation,
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
        const descriptor = {
          first:
            'Ready to test the waters of a potential candidacy by launching a mock campaign on Demodraft?',
          second:
            'First, input your address to see the positions at every level of government that represent your area.',
          third:
            '* Disclaimer: This feature is for registering your campaign to appear on Demodraft. Demodraft does not officially register you with the Federal Election Commission.',
        };
        return descriptor;
      }

      if (this.campaignProgress === 1) {
        const descriptor = {
          first:
            'Here are the available offices we found that you can run your campaign in.',
          second:
            'Select a position you would like to launch your campaign for.',
        };
        return descriptor;
      }

      const position = this.selectedPosition.name;
      if (position) {
        const descriptor = {
          first: `Whenever you're ready, click the large blue button to launch your campaign for ${position}!`,
        };
        return descriptor;
      }
    },
  },
  methods: {
    /////
    /// Step 1 Methods
    //
    async handleSearch(address) {
      try {
        this.isSearching = true;
        this.civicData = await this.getCivicDataFromAddress(address);
        this.positions = this.setPositionDisplayOrder(this.civicData);
        this.$emit('pushStepTwo');
      } catch (error) {
        alert(`Oops, we couldn't find positions for that address!`);
      }
      this.isSearching = false;
    },
    getCivicDataFromAddress(address) {
      return ApiUtil.postAddress({
        username: this.$store.getters.username,
        password: this.$store.getters.password,
        address: address,
      });
    },
    setPositionDisplayOrder({ local, state, country }) {
      return { local, state, country };
    },
    /////
    /// Step 2 Methods
    //
    handlePositionSelected(selectedPosition) {
      this.selectedPosition = selectedPosition;
      this.$emit('pushStepThree');
    },
    /////
    /// Step 3 Methods
    //
    async handleSubmitCampaign() {
      const data = {
        username: this.$store.getters.username,
        scope: this.selectedPosition.scope,
        index: this.selectedPosition.index,
      };

      this.isLaunching = true;
      try {
        await simulateApiCall();
        //await ApiUtil.submitCampaign(data);
        await this.updatePendingCampaign();
        await this.displayConfirmationModal();
        return this.$emit('completeAllSteps', true);
      } catch (error) {
        alert(`Oops, something went wrong launching your campaign.`);
      }
      this.isLaunching = false;
    },
    displayConfirmationModal() {
      const modalMessage = `Thank you for submitting a request to launch your campaign! You will be notified when your application is accepted.`;
      return this.$bvModal.msgBoxOk(modalMessage, {
        title: 'Confirmation',
        size: 'sm',
        buttonSize: 'sm',
        okVariant: 'success',
        headerClass: 'p-2 border-bottom-0',
        footerClass: 'p-2 border-top-0',
        centered: true,
      });
    },
    updatePendingCampaign() {
      this.$store.dispatch('changeCampaignPending');
    }
  },
};
</script>

<style lang="scss" scoped>
.campaign-reg {
  &__description {
    max-width: 800px;
    padding: 1em;
    text-align: center;
    :nth-child(1) {
      font-weight: bold;
      font-size: 1.3rem;
    }

    :nth-child(3) {
      font-style: italic;
    }
  }

  &__steps {
    display: flex;
    justify-content: center;
    padding: 1em 0 2em 0;
  }
}
</style>
