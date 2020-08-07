<template>
  <div>
    <b-container>
      <b-form @submit.prevent="handleSubmit">
        <b-form-group
          id="address-group"
          label="Address"
          label-for="address"
          description="(e.g. 1263 Pacific Ave. Kansas City, KS)"
        >
          <b-form-input
            id="address"
            v-model="internalAddress"
            type="text"
            required
          />
        </b-form-group>
        <b-button type="submit">Search</b-button>
      </b-form>
    </b-container>
  </div>
</template>

<script>
export default {
  name: 'CampaignAddressSearch',
  props: {
    address: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      internalAddress: this.address, // creating copy of props.address to prevent "mutation errors"
    };
  },
  methods: {
    async handleSubmit() {
      this.$emit('handle-submit', this.internalAddress);
    },
  },
};
</script>

<style lang="scss" scoped></style>
