<template>
  <BCard
    :title="politician.name"
    img-src="https://via.placeholder.com/300"
    img-alt="Image"
    img-top
    class="mb-2 politician-card"
  >
    <BButton href="#" variant="Link">Learn More</BButton>
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
  width: 300px;
  height: 425x;
  overflow: hidden;
}
</style>
