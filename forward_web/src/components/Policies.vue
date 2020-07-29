<template>
  <div class="policy">
    <div
      class="policy__card-wrapper"
      v-for="policy in policies"
      :key="policy.id"
    >
      <router-link
        v-bind:to="{
          name: 'PolicyView',
          params: { id: policy.id, description: policy.body },
        }"
        class="policy__route"
      >
        <b-card title="Policy" class="mb-2 policy__card">
          <b-card-text>
            {{ policy.title }}
          </b-card-text>

          <!-- <b-button href="#" variant="primary">Go somewhere</b-button> -->
        </b-card>
      </router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: "Policies",
  props: {
    policies: {
      type: Array,
      required: true,
    },
  },
  methods: {},
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
    // margin: 20px;
    cursor: pointer;
  }

  &__route {
    text-decoration: none;
    color: unset;
  }
}
</style>
