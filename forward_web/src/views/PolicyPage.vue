<template>
  <div>
    <h1>Policy View</h1>

    <p>insert "favorite this policy" icon here</p>

    <h4>Description:</h4>
    <p>{{ policy.body }}</p>

    <CommentList />
  </div>
</template>

<script>
import CommentList from "../components/CommentList";
import { ApiUtil } from "../_utils/api-utils";

export default {
  name: "PolicyPage",
  components: {
    CommentList,
  },
  data() {
    return {
      policy: {},
    };
  },
  async created() {
    this.policy = await ApiUtil.getPolicy(this.$route.params.id);
    await console.log(this.policy);
  },
};
</script>

<style lang="scss" scoped>
div {
  text-align: center;
  padding: 20px;
}
</style>
