<template>
  <BCard
    :title="politician.name"
    img-src="https://i.picsum.photos/id/1062/5092/3395.jpg?hmac=o9m7qeU51uOLfXvepXcTrk2ZPiSBJEkiiOp-Qvxja-k"
    img-alt="Image"
    style="max-width: 20rem;"
    img-top
    class="mb-2 politician-card"
  >
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
import { BCard, BButton } from "bootstrap-vue";

export default {
  name: "PoliticianCard",
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
}
</style>
