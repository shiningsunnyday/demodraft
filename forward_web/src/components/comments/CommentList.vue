<template>
  <div>
    <h1>Comments</h1>
    <CommentForm 
      :updateComments="updateComments"
      :policyId="policyId" 
      :isReply="false"
    ></CommentForm>
    <div 
      class="comments-wrapper"
      v-if="comments.length" 
      v-for="(comment, index) in comments" 
      :key="`comment-${index}`"
    >
      <CommentThread :comment="comment" :updateComments="updateComments"></CommentThread>
    </div>
  </div>
  </div>
</template>

<script>
import { ApiUtil } from "@/_utils/api-utils.js";
import CommentThread from './CommentThread';
import CommentForm from "@/components/comments/CommentForm";

export default {
  name: "CommentList",
  components: {
    CommentThread,
    CommentForm,
  },
  props: {
    policyId: Number,
  },
  data() {
    return {
      comments: [],
      isViewReplies: false,
    };
  },
  async created() {
    try {
      this.comments = await ApiUtil.getPolicyComments(this.policyId);
    } catch (error) {
      alert(`Error ${error.response.status}: Something when wrong fetching this policy's comments`);
      console.log(error);
    }
  },
  methods: {
    async updateComments() {
      // "diffing" allows efficient rerendering - instead of rerendering entire comment section
      this.comments = await ApiUtil.getPolicyComments(
        this.$route.params.id
      );
    }
  }
};
</script>

<style lang="scss" scoped>
.comments-wrapper {
  text-align: start;
  max-width: 700px;
  margin: 0 auto;
}
</style>
