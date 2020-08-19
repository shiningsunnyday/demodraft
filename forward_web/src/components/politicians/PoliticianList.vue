<template>
  <div class="politician-list">
    <div v-for="politician in filteredPoliticians" :key="politician.id">
      <PoliticianCard :politician="politician" />
    </div>
  </div>
</template>

<script>
import PoliticianCard from "./PoliticianCard";

export default {
  name: "PoliticianList",
  components: {
    PoliticianCard,
  },
  props: {
    filteredPoliticians: {
      type: Array,
      required: true,
    },
  },
};
</script>

<style lang="scss" scoped>
.politician-list {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  margin: 20px;
}
</style>
