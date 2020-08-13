<template>
  <b-form-group>
    <b-form-radio-group
      class="positions"
      v-for="(position, keyName) in positions"
      :key="keyName"
    >
      <h4 class="positions__title">{{ keyName.toUpperCase() }}</h4>
      <div class="positions__radio-container">
        <b-form-radio
          v-model="internalSelectedPos"
          v-for="(positionObject, index) in position"
          :key="index"
          :value="{
            name: positionObject.name,
            index: index,
            scope: `${keyName}`,
          }"
        >
          {{ positionObject.name }}
        </b-form-radio>
      </div>
    </b-form-radio-group>
  </b-form-group>
</template>

<script>
export default {
  name: 'CampaignFormGroup',
  props: {
    scope: String,
    positions: Object,
  },
  data() {
    return {
      internalSelectedPos: '',
    };
  },
  watch: {
    internalSelectedPos: function() {
      this.$emit('update-selected-pos', this.internalSelectedPos);
    },
  },
};
</script>

<style lang="scss" scoped>
.positions {
  padding: 1rem 0;
  
  @media screen and (min-width: 768px) {
    display: grid;
    grid-template-columns: 1fr 3fr;
  }

  &__radio-container {
    display: flex;
    flex-direction: column;
  }
}
</style>
