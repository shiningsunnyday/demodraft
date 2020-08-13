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
        <BButton v-if="isPolitician" v-b-modal.modal-endorse @click="handleEndorse">
          Endorse
        </BButton>
      </BCard>
    </b-collapse>
    <b-card-text class="policy__category">
      Category: {{ policy.category }}
    </b-card-text>
  </BCard>
</template>

<script>
import { ApiUtil } from "@/_utils/api-utils";

export default {
  name: 'PolicyCard',
  props: {
    policy: Object,
  },
  data() {
    return {
      isPolitician: false,
    };
  },
  created() {
    const currentUser = this.$store.getters.getUserInfo;
    if (currentUser.approved) {
      this.isPolitician = true;
    }
  },
  methods: {
    async handleEndorse() {
      // maybe get previous stance and populate stance text
      const policyData = {
        name: this.policy.name,
        id: this.policy.id,
      };

      this.$emit('handle-policy-stance', policyData);
    },
  },
};
</script>

<style lang="scss" scoped></style>
