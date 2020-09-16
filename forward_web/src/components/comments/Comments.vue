<template>
  <div>
    <h1>Comments</h1>

    <CommentFormLead 
      :updateComments="updateComments"
      :commentFormId="commentFormId"
      :commentSection="commentSection" 
    />

    <LoadingSpinner v-if="isLoading" />
    <div 
      v-else-if="!isLoading && comments.length" 
      v-for="(comment, index) in comments" 
      :key="`comment-${index}`"
      class="comments-wrapper"
    >
      <CommentThread 
        :comment="comment" 
        :updateComments="updateComments" 
      />
    </div>
  </div>
</template>

<script>
import { ApiUtil } from "@/_utils/api-utils.js";
import CommentThread from './CommentThread';
import CommentFormLead from "@/components/comments/forms/CommentFormLead";

export default {
  name: "Comments",
  components: {
    CommentThread,
    CommentFormLead,
  },
  props: {
    commentFormId: Number,
    commentSection: String,
  },
  data() {
    return {
      comments: [],
      isLoading: true,
    };
  },
  async created() {
    const allComments = await ApiUtil.getComments(
      this.commentFormId, this.commentSection
    );
    
    if (allComments) {
      this.comments = allComments;
    }

    this.isLoading = false;
  },
  methods: {
    async updateComments() {
      const updatedComments = await ApiUtil.getComments(
        this.commentFormId, this.commentSection
      );

      if (updatedComments) {
        this.comments = updatedComments;
      }
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
