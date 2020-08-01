<template>
  <div>
    <h1>Policy View</h1>

    <p>insert "favorite this policy" icon here</p>

    <h4>Description:</h4>
    <p>{{ description }}</p>

    <h5>Comments</h5>
  </div>
</template>

<script>
export default {
  name: "PolicyPage",
  props: {
    description: {
      type: String,
      required: true,
    },
  },
};
</script>

<style lang="scss" scoped>
div {
  text-align: center;
  padding: 20px;
}
</style>
