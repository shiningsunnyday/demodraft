<template>
  <BCard class="mb-2 policy__card">
    <b-card-title>
      <b-button
        variant="link"
        v-b-toggle
        :href="`#collapse-${policy.id}`"
        @click.prevent
      >
        {{ policy.name }}
      </b-button>
    </b-card-title>
    <b-collapse :id="`collapse-${policy.id}`" class="mt-2">
      <b-card>
        <p class="card-text">{{ policy.statement }}</p>
        <b-button variant="link" @click="handleLearnMore">
          Learn more
        </b-button>
      </b-card>
    </b-collapse>
    <b-card-text class="policy__category">
      Category: {{ policy.category }}
    </b-card-text>
  </BCard>
</template>

<script>
import { ApiUtil } from '@/_utils/api-utils';

export default {
  name: 'PolicyCard',
  props: {
    policy: Object,
  },
  methods: {
    handleLearnMore() {
      this.$router.push({ 
        name: 'selected-policy', 
        params: { id: this.policy.id }
      });
    }
  }
};
</script>

<style lang="scss" scoped></style>
