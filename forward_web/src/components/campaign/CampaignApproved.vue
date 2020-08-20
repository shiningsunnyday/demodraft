<template>
  <div class="campaign-details">
    <b-container class="campaign-details__approved-block">
      <h2 class="campaign-details__title">My Campaign</h2>
      <div class="campaign-details__description-block">
        <p class=" campaign-details__politician-name campaign-details--bold">
          {{ politician.firstName }} {{ politician.lastName }}
        </p>
        <p class="campaign-details__position">
          Running for: {{ politician.position }}
        </p>
        <b-button variant="primary" @click="handlePoliticianPage">
          My politician page
        </b-button>
      </div>

      <hr />

      <div class="campaign-details__fundraise-block">
        <p class="campaign-details__actblue-block">
          <span class="campaign-details--bold">ActBlue: </span>
          <a
            class="campaign-details__actblue"
            :href="politician.actblue"
            target="_blank"
            rel="noopener noreferrer"
          >
            {{ politician.actblue }}
          </a>
        </p>
        <p><span class="campaign-details--bold">Goal: </span>${{ politician.fundraiseGoal }}</p>
        <p><span class="campaign-details--bold">Funds Raised: </span>{{ politician.fundraised }}</p>
      </div>
      <hr />
      <b-form @submit.prevent="handleSubmit" class="campaign-details__form">
        <b-form-group label="Actblue" label-for="mycampaign-actblue">
          <b-form-input
            id="mycampaign-actblue"
            label="Actblue"
            v-model="politician.actblue"
            type="text"
            required
          />
        </b-form-group>
        <b-form-group label="Fundraise Goal" label-for="mycampaign-fundraise">
          <b-form-input
            id="mycampaign-fundraise-range"
            v-model="politician.fundraiseGoal"
            type="range"
            min="0"
            max="5000"
            required
          />
          <b-input-group prepend="$" append=".00">
            <b-form-input
              id="mycampaign-fundraise-input"
              v-model="politician.fundraiseGoal"
              type="number"
              min="0"
              max="5000"
              required
            />
          </b-input-group>
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
</template>

<script>
import { ApiUtil } from '@/_utils/api-utils';

export default {
  name: 'CampaignApproved',
  props: {
    politician: Object,
  },
  data() {
    return {
      isApproved: false,
      isUpdated: true,
      isSuccess: false,
      userException: {
        message: '',
        name: 'UserException'
      }
    };
  },
  methods: {
    handlePoliticianPage() {
      this.$router.push({
        name: 'selected-politician',
        params: { id: this.politician.id },
      });
    },
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
        this.isSuccess = true;
        setTimeout(() => {
          this.isSuccess = false;
        }, 1000);
      } catch (error) {
        alert(error);
        console.error('error on updating campaign');
      }
      this.isUpdated = true;
    },
  },
};
</script>

<style lang="scss" scoped>
.campaign-details {
  p {
    padding: 0;
    margin: 0;
  }

  &__title {
    font-size: 2rem;
    text-align: center;
    margin-bottom: 2rem;
  }

  &__politician-name {
    font-size: 1rem;
  }

  &__fundraise-block {
    margin: 1rem 0;
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

  &--bold {
    font-weight: bold;
  }
}
</style>
