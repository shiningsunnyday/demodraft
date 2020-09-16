<template>
  <b-container>
    <b-form autocomplete="on" class="campaign__address-form" @submit.prevent="handleSearch">
      <b-form-group
        id="street-group"
        label="Street Address"
        label-for="street"
        description="(e.g. 1263 Pacific Ave)"
      >
        <b-form-input
          id="street"
          v-model="street"
          autocomplete="street-address"
          type="text"
          required
        />
      </b-form-group>
      <b-form-group
        id="city-group"
        label="City"
        label-for="city"
        description="(e.g. Kansas City)"
      >
        <b-form-input
          id="city"
          v-model="city"
          type="text"
          required
        />
      </b-form-group>
      <b-form-group
        id="state-group"
        label="State"
        label-for="state"
        description="(e.g. KS or Kansas)"
      >
        <b-form-input
          id="state"
          v-model="state"
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
      street: '',
      city: '',
      state: '',
    };
  },
  methods: {
    handleSearch() {
      const data = `${this.street} ${this.city} ${this.state}`;
      this.$emit('handle-search', data);
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
