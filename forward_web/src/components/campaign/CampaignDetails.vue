<template>
  <div class="campaign-details">
    <div v-if="isLoading">
      <b-spinner :variant="'secondary'" label="Loading..."></b-spinner>
    </div>
    <div v-else class="campaign-details__content">
      <div v-if="!isApproved">
        <h1>Thank you for submitting your campaign! 😄</h1>
        <h3>
          Your current submission is: Pending
        </h3>
        <h4>We'll notify you when your submission status is updated</h4>
      </div>

      <b-container v-else class="campaign-details__approved-block">
        <div>
          <h1 class="campaign-details__title">My Campaign</h1>
          <p class="campaign-details__politician-name">
            {{ politician.firstName }} {{ politician.lastName }}
          </p>
          <p class="campaign-details__position">
            Running for: {{ politician.position }}
          </p>
        </div>
        <hr />

        <div class="campaign-details__fundraise-block">
          <p class="campaign-details__actblue-block">
            <span>ActBlue: </span>
            <a
              class="campaign-details__actblue"
              :href="politician.actblue"
              target="_blank"
              rel="noopener noreferrer"
            >
              {{ politician.actblue }}
            </a>
          </p>
          <p><span>Goal: </span>{{ politician.fundraiseGoal }}</p>
          <p><span>Fund Raised: </span>{{ politician.fundraised }}</p>
        </div>

        <b-form @submit.prevent="handleSubmit" class="campaign-details__form">
          <b-form-group
            id="mycampaign-group"
            label="My Campaign"
            label-for="mycampaign"
            description="Update any info for your current campaign"
          >
            <b-form-input
              id="mycampaign"
              v-model="politician.actblue"
              type="text"
              required
            />
            <b-form-input
              id="mycampaign"
              v-model="politician.fundraiseGoal"
              type="text"
              required
            />
          </b-form-group>
          <div v-if="!isSuccess">
            <b-button v-if="isUpdated" type="submit">Update</b-button>
            <b-button v-else disabled>
              <b-spinner small label="Spinning"></b-spinner>
              Updating...
            </b-button>
          </div>
          <b-button v-else variant="success" disabled>Updated!</b-button>
        </b-form>
      </b-container>
    </div>
  </div>
</template>

<script>
import { ApiUtil } from '@/_utils/api-utils';
import { simulateApiCall } from '@/_utils/common-utils';

export default {
  name: 'CampaignDetails',
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
  methods: {
    async handleSubmit() {
      try {
        this.isUpdated = false;
        const user = this.$store.getters.getUserInfo;
        const updated = await ApiUtil.putCampaign({
          politician_id: this.politician.id,
          actblue: this.politician.actblue,
          fundraise_goal: this.politician.fundraiseGoal,
        });
        this.politician.actblue = updated.actblue;
        this.politician.fundraiseGoal = updated.fundraise_goal;
        this.isUpdated = true;
        this.isSuccess = true;
        console.log(updated);

        setTimeout(() => {
          this.isSuccess = false;
        }, 1000);
      } catch (error) {
        alert('Oops, something went wrong updating your campaign!');
        console.error(error);
      }
    },
  },
};
</script>

<style lang="scss" scoped>
.campaign-details {
  font-size: 14px;

  @media screen and (min-width: 768px) {
    font-size: 1rem;
  }

  &__title {
    font-size: 2rem;
    text-align: center;
    margin-bottom: 2rem;
  }

  &__politician-name {
    font-weight: bold;
    font-size: 1rem;
  }

  &__fundraise-block {
    margin: 1rem 0;

    span {
      font-weight: bold;
    }
  }

  &__actblue-block {
    @media screen and (min-width: 768px) {
      display: flex;
      align-items: center;
      span {
        margin-right: 5px;
      }
    }
  }

  &__actblue {
    display: block;
    max-width: 300px;
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;

    @media screen and (min-width: 768px) {
      display: inline-block;
      max-width: 500px;
    }
  }

  p {
    padding: 0;
    margin: 0;
  }
}
</style>
