<template>
  <b-form-group>
    <b-form-radio-group
      v-for="(position, keyName) in positions"
      stacked
    >
      <h4>{{keyName.toUpperCase()}}</h4>
      <b-form-radio
        v-model="internalSelectedPos"
        v-for="(positionObject, index) in position"
        :key="index"
        :value="{ name: positionObject.name, index: index, scope: `${keyName}` }"
      >
        {{ positionObject.name }}
      </b-form-radio>
    </b-form-radio-group>
  </b-form-group>
</template>

<script>
export default {
  name: 'CampaignFormGroup',
  props: {
    scope: String,
    positions: Object
  },
  data() {
    return {
      internalSelectedPos: '',
    };
  },
  watch: {
    internalSelectedPos: function() {
      this.$emit('update-selected-pos', this.internalSelectedPos);
    }
  },
};
</script>

<style lang="scss" scoped></style>
