<template>
  <div>
    <h1>CommentList Component</h1>

    <div v-if="comments.length" class="comments-wrapper">
      <div v-for="comment in comments" :key="comment.id" class="comments-wrapper__comment">
        <p>{{ comment.username }}</p>
        <p>{{ comment.content }}</p>
        <p>Likes: {{ comment.likes }}</p>
        <BButton>Like dis comment</BButton>
      </div>
    </div>
  </div>
</template>

<script>
import { BButton } from "bootstrap-vue";
import { ApiUtil } from "../_utils/api-utils";
// 1. Get list of comments linked to selected PolicyPage's id
// 2. For each comment that exists, created a CommentCard component
// 3. Render each of those CommentCard components

export default {
  name: "CommentList",
  data() {
    return {
      comments: [],
    };
  },
  components: {
    "b-button": BButton,
  },
  methods: {},
  async created() {
    // *** Squashing all policy comments into a single array because it's easier to work with at the moment (need help understanding thread data structure better) ***
    const policyComments = await ApiUtil.getPolicyComments(
      this.$route.params.id
    );

    policyComments.forEach((currArr) => {
      currArr.forEach((currComm) => {
        this.comments.push(currComm);
      });
    });

    // console.log(this.comments);
  },
};
</script>

<style lang="scss" scoped>
.comments-wrapper {
  &__comment {
    border: 1px solid black;
    padding: 10px;
    margin-bottom: 10px;
  }
}
</style>
