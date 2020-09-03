<template>
  <div>
    <h1 class="comment-title">Comments</h1>
    <CommentForm2 
      :updateComments="updateComments"
      :politicianId="politicianId" 
      :isReply="false"
    ></CommentForm2>
    <div v-if="isLoading">Loading...</div>
    <div 
      class="comments-wrapper"
      v-else-if="!isLoading && comments.length" 
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
import CommentForm2 from "@/components/comments/CommentForm2";

export default {
  name: "CommentList2",
  components: {
    CommentThread,
    CommentForm2,
  },
  props: {
    politicianId: Number,
  },
  data() {
    return {
      comments: [],
      isLoading: true,
    };
  },
  async created() {
    try {
      this.comments = await ApiUtil.getPoliticianComments(this.politicianId);
    } catch (error) {
      alert(`Error ${error.response.status}: Something when wrong fetching this policy's comments`);
      console.log(error);
    }
    this.isLoading = false;
  },
  methods: {
    async updateComments() {
      this.comments = await ApiUtil.getPoliticianComments(
        this.$route.params.id
      );
    }
  }
};
</script>

<style lang="scss" scoped>
.comment-title {
  display: flex;
  justify-content: center;
}
.comments-wrapper {
  text-align: start;
  max-width: 700px;
  margin: 0 auto;
}
</style>
