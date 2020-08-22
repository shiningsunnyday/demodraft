<template>
  <div class="policy-list-container">
    <div
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
.policy-list-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;

  &__route {
    text-decoration: none;
    color: unset;
  }
}
</style>
