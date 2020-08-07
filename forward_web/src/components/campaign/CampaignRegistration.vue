<template>
  <div>
    <h1>CampaignRegistration</h1>

    <b-container>
      <b-form @submit.prevent="handleSubmit">
        <b-form-group
          id="address-group"
          label="Address"
          label-for="address"
          description="(e.g. 1263 Pacific Ave. Kansas City, KS)"
        >
          <b-form-input id="address" v-model="address" type="text" required />
        </b-form-group>
        <b-button type="submit">Launch</b-button>
      </b-form>
    </b-container>
    <pre>{{ civicData }}</pre>
  </div>
</template>

<script>
import * as Config from "@/config.json";

export default {
  name: "CampaignRegistration",
  data() {
    return {
      civicData: undefined,
      address: "",
      status: null
    };
  },
  methods: {
    handleSubmit() {
      // POST /address/ 
      // example request: {"address":"1263 Pacific Ave. Kansas City, KS"}
      console.log("yippie!");
    },
  },
};
</script>

<style lang="scss" scoped></style>
