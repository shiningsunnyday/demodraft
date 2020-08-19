<template>
  <div class="policy">
    <div
      class="policy__card-wrapper"
      v-for="policy in filteredPolicies"
      :key="policy.id"
    >
      <PolicyCard :policy="policy"></PolicyCard>
    </div>
  </div>
</template>

<script>
import { BCard, BButton } from 'bootstrap-vue';
import PolicyCard from './PolicyCard';
import { ApiUtil } from '@/_utils/api-utils';

export default {
  name: 'PolicyList',
  components: {
    'b-button': BButton,
    'b-card': BCard,
    PolicyCard,
  },
  props: {
    filteredPolicies: {
      type: Array,
      required: true,
    },
  },
};
</script>

<style lang="scss" scoped>
.policy {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;

  &__card-wrapper {
    margin: 20px;
  }

  &__card {
    width: 300px;
    @media screen and (min-width: 768px) {
      width: 455px;
    }
    //cursor: pointer;
  }

  &__route {
    text-decoration: none;
    color: unset;
  }

  &__category {
    margin-top: 1em;
  }
}
</style>
