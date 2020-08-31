<template>
  <b-container>
    <b-form class="campaign__address-form" @submit.prevent="handleSearch">
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

      <b-button v-if="isSearching" class="campaign__search-button" block disabled>
        <b-spinner small type="grow"></b-spinner>
        Searching...
      </b-button>

      <b-button 
        v-else 
        type="submit" 
        class="campaign__search-button" 
        variant="primary"
        block
      >
        Search
      </b-button>
    </b-form>
  </b-container>
</template>

<script>
export default {
  name: 'CampaignAddressSearch',
  props: {
    isSearching: {
      type: Boolean
    }
  },
  data() {
    return {
      internalAddress: '',
    };
  },
  methods: {
    handleSearch() {
      this.$emit('handleSearch', this.internalAddress);
    },
  },
};
</script>

<style lang="scss" scoped>
.campaign {
  &__address-form {
    @media screen and (min-width: 768px) {
      width: 500px;
      margin: 0 auto;
    }
  }

  &__search-button {
    width: 200px;
    margin: 0 auto;
  }
}
</style>
