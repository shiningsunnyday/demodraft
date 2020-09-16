<template>
  <LoadingSpinner v-if="isLoading"></LoadingSpinner>
  <b-container v-else class="selected-politician">
    <div class="selected-politician__button-container">
      <div class="selected-politician__back-button-container">
        <b-button size="sm" @click="handleBackButton">
          Back to Politicians
        </b-button>
      </div>

      <div class="selected-politician__follow-button-container">
        <b-button size="sm" disabled> <BIconPersonPlus /> Follow </b-button>
      </div>
    </div>

    <div class="selected-politician__top">
      <h1>{{ politician.first }} {{ politician.last }}</h1>

      <div class="selected-politician__img-wrapper">
        <img src="@/_assets/politician-placeholder.jpg" />
      </div>

      <div class="selected-politician__description">
        <p>Running for {{ politician.position }}</p>

        <p v-if="politician.actblue" class="selected-politician__actblue-link">
          <a
            :href="politician.actblue"
            target="_blank"
            rel="noopener noreferrer"
          >
            Actblue
          </a>
        </p>
      </div>
    </div>

    <div class="selected-politician__bottom">
      <h3>Policies I Endorse</h3>

      <LoadingSpinner v-if="isLoading"></LoadingSpinner>

      <div
        v-else
        v-for="policy in endorsed"
        v-bind:key="policy.id"
        class="selected-politician__list"
      >
        <b-button
          @click="handleSelectedPolicy(policy.id)"
          variant="link"
          class="selected-politician__route"
        >
          {{ policy.name }}
        </b-button>

        <p class="selected-politician__message">
          "{{ policy.message }}" - {{ politician.first }} {{ politician.last }}
        </p>
      </div>
    </div>
    <hr />
    <div class="selected-politician__comments">
      <Comments :commentFormId="politician.id" :commentSection="'politician'" />
    </div>
  </b-container>
</template>

<script>
import { ApiUtil } from '@/_utils/api-utils';
import { BIconPersonPlus } from 'bootstrap-vue';
import Comments from '@/components/comments/Comments';

export default {
  name: 'SelectedPolitician',
  components: {
    Comments,
    BIconPersonPlus,
  },
  data() {
    return {
      politician: {},
      stances: [],
      isLoading: true,
    };
  },
  async created() {
    const user = this.$store.getters.userState;
    const modifiedPolitician = this.$store.getters.getPolitician;
    const politicianId = Number(this.$route.params.id);

    // use politician state for current approved user
    if (modifiedPolitician.id === politicianId) {
      this.politician = modifiedPolitician;
      this.stances = this.politician.endorsed;
    } else {
      // fetch politician for regular users
      this.politician = await ApiUtil.getSelectedPolitician(politicianId);
      this.stances = await ApiUtil.getAllStances(this.politician.id);
      this.politician.position = this.politician.name;
    }
    
    this.isLoading = false;
  },
  computed: {
    endorsed() {
      if (this.stances.length > 0) {
        const policySet = new Set();
        const endorsed = [];
        for (let stance of this.stances) {
          if (!policySet.has(stance.polict_id)) {
            policySet.add(stance.policy_id);
            endorsed.push({
              name: stance.policy_name,
              message: stance.message,
              id: stance.policy_id,
            });
          }
        }
        return endorsed;
      }
    },
  },
  methods: {
    handleSelectedPolicy(policyId) {
      this.$router.push({
        name: 'selected-policy',
        params: { id: policyId },
      });
    },
    handleBackButton() {
      //Go back to politicians page
      this.$router.push({
        name: 'politician-page',
      });
    },
  },
};
</script>

<style lang="scss" scoped>
@mixin flex-column-center {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.selected-politician {
  font-size: 14px;

  @media screen and (min-width: 768px) {
    @include flex-column-center;
    font-size: 1rem;
    > * {
      padding: 1rem;
    }
  }

  &__button-container {
    display: flex;
    justify-content: space-between;
    width: 80%;
    margin: 0 auto;
    padding: 1rem;
  }

  &__follow-button-container {
    display: flex;
    justify-content: flex-end;

    @media screen and (min-width: 768px) {
      //commented out width: 75%; because
      //makes button fat at specific view port
      //width: 75%;
    }
  }

  &__top {
    @include flex-column-center;
    @media screen and (min-width: 768px) {
      width: 500px;
    }
  }

  &__bottom {
    @include flex-column-center;
    @media screen and (min-width: 768px) {
      width: 500px;
    }
  }

  &__comments {
    width: 100%;
    text-align: center;
  }

  &__actblue-link {
    text-align: center;
    text-decoration: underline;
    font-size: 1.2rem;
  }

  &__img-wrapper {
    max-width: 500px;
    max-height: 700px;
  }

  img {
    width: 100%;
  }

  &__description {
    margin: 1rem;
  }

  &__list {
    @include flex-column-center;
    text-align: center;
  }
}
</style>
