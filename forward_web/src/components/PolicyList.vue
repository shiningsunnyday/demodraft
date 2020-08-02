<template>
  <div class="policy">
    <div
      class="policy__card-wrapper"
      v-for="policy in filteredPolicies"
      :key="policy.id"
    >
      <!-- Move this into own component later -->
      <BCard class="mb-2 policy__card">
        <b-card-title>
          <b-button
            v-b-toggle
            :href="`#collapse-${policy.id}`"
            @click.prevent
          >
            {{ policy.name }}
          </b-button>
        </b-card-title>
        <b-collapse :id="`collapse-${policy.id}`" class="mt-2">
          <BCard>
            <p class="card-text">{{ policy.statement }}</p>
            <BButton variant="link">
              <router-link
                class="policy__route"
                v-bind:to="{
                  name: 'policy-page',
                  params: {
                    id: policy.id,
                  },
                }"
              >
                Learn more
              </router-link>
            </BButton>
          </BCard>
        </b-collapse>
        <b-card-text class="policy__category"> 
          Category: {{ policy.category }} 
        </b-card-text>
      </BCard>
    </div>
  </div>
</template>

<script>
import { BCard, BButton } from 'bootstrap-vue';

export default {
  name: 'PolicyList',
  components: {
    'b-button': BButton,
    'b-card': BCard,
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
