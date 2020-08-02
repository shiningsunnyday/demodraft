<template>
  <div>
    <h1>{{ policy.name }}</h1>

    <button @click="this.likePolicy">{{ `${this.likes} likes` }}</button>
    
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
  methods: {
    async likePolicy() {
      this.likes = await ApiUtil.policyLike(this.$route.params.id);
    }
  },
  data() {
    return {
      likes: 0,
      policy: {},
    };
  },
  async created() {
    this.policy = await ApiUtil.getPolicy(this.$route.params.id);
    this.likes = this.policy.likes;
  }
};
</script>

<style lang="scss" scoped>
div {
  text-align: center;
  padding: 20px;
}
</style>
