<template>
  <BCard
    :title="politician.name"
    img-src="https://i.picsum.photos/id/1062/5092/3395.jpg?hmac=o9m7qeU51uOLfXvepXcTrk2ZPiSBJEkiiOp-Qvxja-k"
    img-alt="Image"
    style="max-width: 20rem;"
    img-top
    class="mb-2 politician-card"
  >
    <b-card-text>
      <BIconBuilding class="politician-card__icon" :scale="1.5" />
      {{ politician.first }} {{ politician.last }}
    </b-card-text>

    <BButton href="#" variant="Link">
      <router-link
        class="politician-card__route"
        v-bind:to="{
          name: 'selected-politician',
          params: {
            id: politician.id,
          },
        }"
      >
        Learn More
      </router-link>
    </BButton>
  </BCard>
</template>

<script>
import { BIconBuilding } from "bootstrap-vue";
import { BCard, BButton } from "bootstrap-vue";

export default {
  name: "PoliticianCard",
  components: {
    BIconBuilding,
  },
  props: {
    politician: {
      type: Object,
      required: true,
    },
  },
};
</script>

<style lang="scss" scoped>
.politician-card {
  margin: 20px;

  &__icon {
    margin-right: 8px;
  }
}
</style>
