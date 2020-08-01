<template>
  <div>
    <h1>{{ policy.name }}</h1>

    <p>insert "favorite this policy" icon here</p>

    <h4>{{ policy.statement }}</h4>
    <p>{{ policy.description }}</p>

    <CommentList />
  </div>
</template>

<script>
import CommentList from "../components/CommentList";
import { ApiUtil } from "../_utils/api-utils";

export default {
  name: "policy-page",
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
  },
};
</script>

<style lang="scss" scoped>
div {
  text-align: center;
  padding: 20px;
}
</style>
