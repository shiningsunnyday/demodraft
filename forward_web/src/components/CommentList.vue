<template>
  <div>
    <h1>CommentList Component</h1>

    <div v-if="comments.length" class="comments-wrapper">
      <div v-for="comment in comments" :key="comment.id">
        <ul>
          <li>{{ comment }}</li>
        </ul>
      </div>
    </div>

    <button>View Comments</button>
  </div>
</template>

<script>
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
  methods: {},
  async created() {
    // *** Squashing all policy comments into a single array because it's easier to work with at the moment (need help understanding thread data structure better) ***
    const policyComments = await ApiUtil.getPolicyComments(this.$route.params.id);

    policyComments.forEach((currArr) => {
      currArr.forEach((currComm) => {
        this.comments.push(currComm);
      });
    });
    
    console.log(this.comments);
  },
};
</script>

<style lang="scss" scoped></style>
