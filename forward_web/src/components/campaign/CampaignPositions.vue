<template>
  <b-form>
    <b-form-group>
      <b-form-radio-group
        class="positions"
        v-for="(position, keyName) in positions"
        :key="keyName"
      >
        <h4 class="positions__title">{{ keyName.toUpperCase() }}</h4>
        <div class="positions__radio-container">
          <b-form-radio
            v-model="selectedPosition"
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
    <div class="positions__button-group">
      <b-button @click="$emit('handleBack')">
        Back
      </b-button>
      <b-button
        v-if="isPositionSelected"
        @click="handleNext"
        variant="primary"
      >
        Next
      </b-button>
      <b-button v-else disabled>Next</b-button>
    </div>
  </b-form>
</template>

<script>
export default {
  name: 'CampaignPositions',
  props: {
    scope: String,
    positions: Object,
  },
  data() {
    return {
      selectedPosition: {},
    };
  },
  computed: {
    isPositionSelected() {
      const { index } = this.selectedPosition;
      return typeof index !== 'undefined';
    },
  },
  methods: {
    handleNext() {
      const data = this.selectedPosition;
      this.$emit('handlePositionSelected', data);
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

  &__button-group {
    :nth-child(1) {
      margin-right: 8px;
    }
  }
}
</style>
