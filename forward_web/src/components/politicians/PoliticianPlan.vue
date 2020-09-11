<template>
  <b-container>
    <h1>Politician Plan</h1>
    <div v-if="hasPlan">
      <b-table striped hover :items="items"></b-table>
      <div v-if="isPolitician">edit</div>
    </div>
    <div v-else>
      This politician has no plan, boo
    </div>
  </b-container>
</template>

<script>
export default {
  name: 'PoliticianPlan',
  props: {
    id: String,
    politician: Object,
    isPushed: Boolean
  },
  data() {
    return {
      items: [
      ],
    };
  },
  created() {
    // TODO - fetch politician plan from id
    // fill this.items with response
    
  },
  computed: {
    isPolitician() {
      const user = this.$store.getters.userState;
      return user.approved;
    },
    hasPlan() {
      return this.items.length >= 1;
    }
  },
};
</script>

<style lang="scss" scoped></style>
