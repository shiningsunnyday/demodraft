<template>
  <BCard
    :title="`${politician.first} ${politician.last}`"
    style="max-width: 20rem;"
    img-top
    class="mb-2 politician-card"
  >
    <b-card-img :src="require('../../_assets/politician-placeholder.jpg')" alt="Image of politician" />
    <b-card-text>
      <BIconBuilding class="politician-card__icon" :scale="1.5" />
      {{ politicianLocation }}
    </b-card-text>

    <BButton href="#" variant="Link">
      <router-link
        :to="{
          name: 'selected-politician',
          params: {
            id: politician.id,
          },
        }"
        class="politician-card__route"
      >
        Learn More
      </router-link>
    </BButton>
  </BCard>
</template>

<script>
import { BIconBuilding } from 'bootstrap-vue';
import { BCard, BButton } from 'bootstrap-vue';
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
}
</style>
