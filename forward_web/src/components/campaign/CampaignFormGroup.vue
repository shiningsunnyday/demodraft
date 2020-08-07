<template>
  <!-- <b-form-group :label="label"> -->
  <!-- <b-form-radio-group stacked> -->
  <div>
    <b-form-radio
      @change="selectPos"
      v-model="internalSelectedPos"
      v-for="(position, index) in positions"
      :key="index"
      :value="{ name: position.name, index: index, scope: `${label}` }"
    >
      {{ position.name }}
    </b-form-radio>
  </div>
  <!-- </b-form-radio-group> -->
  <!-- </b-form-group> -->
</template>

<script>
export default {
  name: 'CampaignFormGroup',
  props: {
    label: {
      type: String,
    },
    selectedPos: {
      type: Object,
    },
    positions: {
      type: Array,
    },
  },
  data() {
    return {
      internalSelectedPos: this.selectedPos, // creating copy of props.selectedPos to prevent "mutation errors"
    };
  },
  methods: {
    selectPos() {
      this.$emit('update-selected-pos', this.internalSelectedPos);
    },
  },
};
</script>

<style lang="scss" scoped></style>
