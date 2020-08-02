<template>
  <div class="policy">
    <div
      class="policy__card-wrapper"
      v-for="policy in filteredPolicies"
      :key="policy.id"
    >
      <router-link
        class="policy__route"
        v-bind:to="{
          name: 'policy-page',
          params: {
            id: policy.id
          },
        }"
      >
        <BCard v-bind:title="policy.name" class="mb-2 policy__card">
          <b-card-text>
            Category: {{ policy.category }}
          </b-card-text>
          <b-card-text>
            {{ policy.title }}
          </b-card-text>
          <BButton>Go somewhere</BButton>
        </BCard>
      </router-link>
    </div>
  </div>
</template>

<script>
import { BCard, BButton } from "bootstrap-vue";

export default {
  name: "PolicyList",
  components: {
    "b-button": BButton,
    "b-card": BCard,
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
    height: 300px;
    cursor: pointer;
  }

  &__route {
    text-decoration: none;
    color: unset;
  }
}
</style>
