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
      <CommentThread 
        :comment="comment" 
      ></CommentThread>
    </div>
    <CommentThread :comment="comment"></CommentThread>
  </div>
  </div>
</template>

<script>
import { BButton, BIcon, BIconHandThumbsUp } from "bootstrap-vue";
import { ApiUtil } from "@/_utils/api-utils.js";
import CommentThread from './CommentThread';
import CommentForm from "@/components/comments/CommentForm";

export default {
  name: "CommentList",
  components: {
    "b-button": BButton,
    BIcon,
    BIconHandThumbsUp,
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
    this.comments = await ApiUtil.getPolicyComments(
      this.$route.params.id
    );
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
