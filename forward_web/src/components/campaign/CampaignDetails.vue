<template>
  <div>
    <h1>CampaignDetails</h1>
    <div v-if="!isApproved">
      <h1>Thank you for submitting your campaign! 😄</h1>
      <h3>
        Your current submission is: Pending
      </h3>
      <h4>We'll notify you when your submission status is updated</h4>
    </div>

    <div v-if="isApproved">
      <h1>Your Campaign Info</h1>
      <p>Running for: {{ campaign.name }}</p>
      <hr />

      <ul>
        <li>ActBlue: <a :href="campaign.actblue" target="_blank" rel="noopener noreferrer">{{ campaign.actblue }}</a></li>
        <li>Fundraise Goal: {{ campaign.fundraise_goal }}</li>
        <li>Funds Raised: {{ campaign.fundraised }}</li>
      </ul>
      <b-form @submit.prevent="handleSubmit">

        <b-form-group
          id="mycampaign-group"
          label="My Campaign"
          label-for="mycampaign"
          description="Update any info for your current campaign"
        >
          <b-form-input
            id="mycampaign"
            v-model="actblue"
            type="text"
            required
          />
          <b-form-input
            id="mycampaign"
            v-model="fundraiseGoal"
            type="text"
            required
          />
        </b-form-group>
        <b-button type="submit">Update</b-button>
      </b-form>
    </div>
  </div>
</template>

<script>
import { ApiUtil } from '@/_utils/api-utils';

export default {
  name: 'CampaignDetails',
  data() {
    return {
      user: {},
      campaign: {},
      actblue: "",
      fundraiseGoal: 0,
      fakeApproved: false,
    };
  },
  async created() {
    const currentUser = this.$store.getters.getUserInfo;
    if (currentUser.approved) {
      this.campaign = await ApiUtil.getCampaign(currentUser.politician_id);
      this.fundraiseGoal = this.campaign.fundraise_goal;
      this.actblue = this.campaign.actblue;
    }

  },
  computed: {
    isApproved() {
      const currentUser = this.$store.getters.getUserInfo;

      // campaign never launched
      // redundant guard clause for now
      if (typeof currentUser.approved === 'undefined') {
        return false;
      }

      return currentUser.approved;
    },
    
  },
  methods: {
    async handleSubmit(event) {
      const currentUser = this.$store.getters.getUserInfo;
      try {
        const response = await ApiUtil.putCampaign({
          politician_id: currentUser.politician_id,
          actblue: this.actblue,
          fundraise_goal: this.fundraiseGoal
        });
        this.campaign = await ApiUtil.getCampaign(currentUser.politician_id);
      } catch (error) {
        console.log(error.message);
      }
    }
  }
};
</script>

<style lang="scss" scoped></style>
