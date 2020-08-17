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
      <BCard>
        <p class="card-text">{{ policy.statement }}</p>
        <BButton variant="link" @click="handleLearnMore">
          Learn more
        </BButton>
      </BCard>
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
    async handleLearnMore() {
      try {
        const selectedPolicy = await ApiUtil.getPolicy(this.policy.id);
        this.$router.push({ 
          name: 'selected-policy', 
          params: { 
            id: this.policy.id, 
            policy: selectedPolicy 
          }
        });
      } catch (error) {
        alert(`Error ${error.response.status}: Something when wrong fetching this policy`);
        console.log(error);
      }
    }
  }
};
</script>

<style lang="scss" scoped></style>
