<template>
  <b-card
    :title="`${politician.first} ${politician.last}`"
    style="max-width: 20rem;"
    img-top
    class="mb-2 politician-card"
  >
    <b-card-img
      :src="require('../../_assets/politician-placeholder.jpg')"
      alt="Image of politician"
    />
    <b-card-text>
      <BIconBuilding class="politician-card__icon" :scale="1.5" />
      {{ politicianLocation }}
    </b-card-text>

    <div class="politician-card__buttons">
      <b-button variant="link" @click="handleLearnMore">
        Learn More
      </b-button>
      <b-button variant="link" @click="handleViewPlan">
        View Plan
      </b-button>
    </div>
  </b-card>
</template>

<script>
import { BIconBuilding } from 'bootstrap-vue';
import { states } from '@/_utils/common-utils.js';

export default {
  name: 'PoliticianCard',
  components: {
    BIconBuilding,
  },
  props: {
    politician: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      states: [],
      politicianLocation: '',
    };
  },
  created() {
    this.politicianLocation = this.politician.state;
  },
  methods: {
    handleLearnMore() {
      this.$router.push({
        name: 'selected-politician',
        params: { id: this.politician.id },
      });
    },
    handleViewPlan() {
      const politicianId = this.politician.id.toString();
      this.$router.push({
        name: 'politician-plan',
        params: { 
          id: politicianId,
          politician: this.politician,
          isPushed: true
        },
      });
    },
  },
};
</script>

<style lang="scss" scoped>
.politician-card {
  margin: 20px;

  .card-text {
    margin-top: 1rem;
  }

  &__icon {
    margin-right: 8px;
  }

  &__buttons {
    display: inline-flex;
    flex-direction: column;
  }
}
</style>
