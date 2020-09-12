<template>
  <div class="campaign-details">
    <b-container class="campaign-details__approved-block">
      <h2 class="campaign-details__title">My Campaign</h2>
      <div class="campaign-details__description-block">
        <p class=" campaign-details__politician-name campaign-details--bold">
          {{ politician.first }} {{ politician.last }}
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
        <p>
          <span class="campaign-details--bold">Goal: </span>${{
            politician.fundraiseGoal
          }}
        </p>
        <p>
          <span class="campaign-details--bold">Funds Raised: </span
          >{{ politician.fundraised }}
        </p>
      </div>

      <hr />

      <b-form
        @submit.prevent="handleUpdateCampaign"
        class="campaign-details__form"
      >
        <b-form-group
          label="Actblue:"
          label-for="mycampaign-actblue"
        >
          <b-form-input
            id="mycampaign-actblue"
            label="Actblue"
            v-model="$v.politician.actblue.$model"
            type="text"
            placeholder="Please enter an ActBlue donation campaign URL"
          />
          <p class="error" v-if="!$v.politician.actblue.required">
            This field is required
          </p>
          <p class="error" v-else-if="!$v.politician.actblue.isActBlueURL">
            Only an ActBlue donation URL is allowed
          </p>
        </b-form-group>
        <b-form-group
          label="Fundraise Goal:"
          label-for="mycampaign-fundraise"
          description="To be FEC compliant, max goal is $5000"
        >
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

        <!-- Update Button Views -->
        <div v-if="!isSuccess">
          <div v-if="!$v.politician.actblue.isActBlueURL">
            <b-button disabled>Update</b-button>
            <p>Please enter valid URL</p>
          </div>

          <b-button v-else-if="!isUpdating" type="submit">Update</b-button>
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
import { required } from 'vuelidate/lib/validators';

export default {
  name: 'CampaignApproved',
  props: {
    politician: Object,
  },
  data() {
    return {
      isApproved: false,
      isUpdating: false,
      isSuccess: false,
      willPrepend: false,
    };
  },
  validations: {
    politician: {
      actblue: {
        required,
        isActBlueURL(url) {
          // Checks if the user entered an ActBlue URL for their campaign
          if (url.toLowerCase().indexOf('https://') === 0) {
            if (
              this.politician.actblue.slice(8, 27) !== 'secure.actblue.com/'
            ) {
              return false;
            }
          } else {
            if (
              this.politician.actblue.slice(0, 19) !== 'secure.actblue.com/'
            ) {
              return false;
            } else {
              // if 'secure.actblue.com/' exists, prepend 'https://' to it
              this.willPrepend = true;
            }
          }

          return true;
        },
      },
    },
  },
  methods: {
    handlePoliticianPage() {
      this.$router.push({
        name: 'selected-politician',
        params: { id: this.politician.id },
      });
    },
    /////
    /// Campaign update methods
    //
    async handleUpdateCampaign() {
      // if 'secure.actblue.com/' exists, prepend 'https://' to it
      if (this.willPrepend) {
        this.politician.actblue = 'https://' + this.politician.actblue;
        this.willPrepend = false;
      }

      this.isUpdating = true;

      try {
        const updatedCampaign = await this.updateCampaign();
        await this.updatePoliticianStore(updatedCampaign);
        this.handleSuccessDelay();
      } catch (error) {
        alert(error);
        console.error('error on updating campaign');
      }

      this.isUpdating = false;
    },
    updateCampaign() {
      return ApiUtil.putCampaign({
        politician_id: this.politician.id,
        actblue: this.politician.actblue,
        fundraise_goal: this.politician.fundraiseGoal,
      });
    },
    updatePoliticianStore(updatedCampaign) {
      this.$store.dispatch('updateCampaign', {
        actblue: updatedCampaign.actblue,
        fundraiseGoal: updatedCampaign.fundraise_goal,
      });
    },
    handleSuccessDelay() {
      this.isSuccess = true;

      setTimeout(() => {
        this.isSuccess = false;
      }, 1000);
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

  &__approved-block {
    margin-bottom: 50px;
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

  .error {
    font-size: 1rem;
    color: rgb(246, 68, 68);
  }
}
</style>
