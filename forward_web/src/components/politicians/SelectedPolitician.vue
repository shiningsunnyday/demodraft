<template>
  <b-container class="selected-politician">
    <div class="selected-politician__left">
      <h1>{{ politician.first }} {{ politician.last }}</h1>
      <div class="selected-politician__img-wrapper">
        <img
          src="https://i.picsum.photos/id/1025/4951/3301.jpg?hmac=_aGh5AtoOChip_iaMo8ZvvytfEojcgqbCH7dzaz-H8Y"
        />
      </div>
      <div class="selected-politician__description">
        <p>Running for {{ politician.name }}</p>
        <p v-if="politician.actblue">Actblue:
          <a :href="politician.actblue" target="_blank" rel="noopener noreferrer">{{ politician.actblue }}</a>
        </p>
      </div>
    </div>
    
    <div class="selected-politician__right">
      <h3>Endorsed</h3>
      <div v-if="isLoading" class="loading-spinner">
        <b-spinner label="Loading..."></b-spinner>
      </div>
      <div 
        v-else 
        v-for="policy in endorsed" v-bind:key="policy.id"
        class="selected-politician__list" 
      >
        <b-button 
          @click="handleSelectedPolicy(policy.id)"
          variant="link"
          class="selected-politician__route"
        >
          {{ policy.name }}
        </b-button>
        <p class="selected-politician__message">{{ policy.message }}</p>
      </div>
    </div>
  </b-container>
</template>

<script>
import { ApiUtil } from '@/_utils/api-utils';

export default {
  name: 'SelectedPolitician',
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
    this.isLoading = false;
  },
  methods: {
    handleSelectedPolicy(policyId) {
      this.$router.push({ 
        name: 'selected-policy', 
        params: { id: policyId }
      });
    }
  }
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

  @media screen and (min-width: 1280px) {
    display: flex;
    font-size: 1rem;
    > * {
      padding: 1rem;
    }
  }

  &__left{
    @include flex-column-center;
    @media screen and (min-width: 1280px) {
      width: 500px;
    }
  }

  &__right {
    @include flex-column-center;
    @media screen and (min-width: 1280px) {
      width: 500px;
    }
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
