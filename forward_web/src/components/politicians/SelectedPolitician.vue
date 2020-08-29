<template>
  <LoadingSpinner v-if="isLoading"></LoadingSpinner>
  <b-container v-else class="selected-politician">
    <div class="selected-politician__follow-button-container">
      <b-button size="sm"> <BIconPersonPlus /> Follow </b-button>
    </div>

    <div class="selected-politician__top">
      <h1>{{ politician.first }} {{ politician.last }}</h1>

      <div class="selected-politician__img-wrapper">
        <img
          src="https://i.picsum.photos/id/1025/4951/3301.jpg?hmac=_aGh5AtoOChip_iaMo8ZvvytfEojcgqbCH7dzaz-H8Y"
        />
      </div>

      <div class="selected-politician__description">
        <p>Running for {{ politician.name }}</p>

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
      <h3>Endorsed</h3>

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

        <p class="selected-politician__message">"{{ policy.message }}"</p>
      </div>
    </div>
    <hr />
    <div class="selected-politician__comments">
      <CommentList2 :politicianId="politician.id"></CommentList2>
    </div>
  </b-container>
</template>

<script>
import { ApiUtil } from '@/_utils/api-utils';
import LoadingSpinner from '@/components/_common/LoadingSpinner';
import { BIconPersonPlus } from 'bootstrap-vue';
import CommentList2 from '@/components/comments/CommentList2';

export default {
  name: 'SelectedPolitician',
  components: {
    CommentList2,
    LoadingSpinner,
    BIconPersonPlus,
  },
  data() {
    return {
      politician: {},
      endorsed: [],
      stances: [],
      isLoading: true,
    };
  },
  async created() {
    this.politician = await ApiUtil.getSelectedPolitician(
      this.$route.params.id
    );

    const stanceResponse = await ApiUtil.getStance(this.politician.id);
    this.stances = stanceResponse.data;

    if (this.stances.length > 0) {
      const policySet = new Set();
      this.stances.forEach((stance) => {
        if (!policySet.has(stance.policy_id)) {
          policySet.add(stance.policy_id);
          this.endorsed.push({
            name: stance.policy_name,
            message: stance.message,
            id: stance.policy_id,
          });
        }
      });
    }

    this.isLoading = false;
  },
  methods: {
    handleSelectedPolicy(policyId) {
      this.$router.push({
        name: 'selected-policy',
        params: { id: policyId },
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

  &__follow-button-container {
    display: flex;
    justify-content: flex-end;

    @media screen and (min-width: 768px) {
      width: 75%;
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

  &__comments{
    width: 100%;
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
