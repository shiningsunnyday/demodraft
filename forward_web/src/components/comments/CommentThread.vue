<template>
  <div class="comments-wrapper__comment">
    <div v-if="isLoading">
      <CommentCardPlaceholder />
    </div>
    <div v-else>
      <!-- Leading comment -->
      <CommentCard
        :comment="comment"
        :prop="cardProps"
        @handleViewReplies="handleViewReplies"
        @updateRepliesView="updateRepliesView"
        @deleteThread="deleteThread"
        @deleteComment="deleteComment"
      ></CommentCard>
      <!-- End leading comment -->

      <!-- Replies to leading comment -->
      <div 
        v-if="cardProps.isViewingReplies" 
        v-for="(reply, index) in replies" 
        :key="reply.id"
      >
        <CommentCard
          :comment="reply"
          :index="index"
          :prop="cardProps"
          @handleViewReplies="handleViewReplies"
          @updateRepliesView="updateRepliesView"
          @deleteThread="deleteThread"
          @deleteComment="deleteComment"
          :className="`comments-wrapper__sub-comment`"
        ></CommentCard>
      </div>
      <!-- End replies to leading comment -->
    </div>
  </div>
</template>

<script>
import CommentCard from './CommentCard';
import CommentCardPlaceholder from './CommentCardPlaceholder';
import CommentForm from '@/components/comments/CommentForm';
import { ApiUtil } from '@/_utils/api-utils.js';

export default {
  name: 'CommentThread',
  components: {
    CommentCard,
    CommentForm,
    CommentCardPlaceholder
  },
  props: {
    comment: Object,
    className: String,
    updateComments: Function,
  },
  data() {
    return {
      replies: [],
      replyComment: {}, // in progress
      isLoading: true,
      cardProps: {
        isViewingReplies: false,
        hasReplies: false,
        threadId: 0,
        isMod: false, // change this to true for testing
      }
    };
  },
  async created() {
    const thread = await ApiUtil.getThreadFromComment(this.comment.thread_id);
    this.cardProps.threadId = this.comment.thread_id;
    this.cardProps.hasReplies = thread.replies.length > 0 ? true : false;
    this.replies = thread.replies;
    this.isLoading = false;
  },
  methods: {
    async updateThread(threadId) {
      const thread = await ApiUtil.getThreadFromComment(threadId);
      this.replies = thread.replies;
    },
    handleViewReplies(threadId) {
      // only make api call when viewing replies
      if (!this.cardProps.isViewingReplies) {
        this.updateThread(threadId);
      }
      this.cardProps.isViewingReplies = !this.cardProps.isViewingReplies;
    },
    updateRepliesView() {
      this.updateThread(this.cardProps.threadId);
      // only open replies if closed
      if (!this.cardProps.isViewingReplies) { 
        this.cardProps.isViewingReplies = !this.cardProps.isViewingReplies;
      }
      this.cardProps.hasReplies = true;
    },
    async deleteThread(threadId) {
      console.log('delete thread: ', threadId);
      // await ApiUtil.deleteThread(threadId, this.$store.getters.username);
      // this.updateComments();
    },
    async deleteComment(index) {
      let id;
      if (index == 0) {
        id = this.comment.id;
      } else {
        id = this.replies[index-1].id;
      }
      console.log('delete comment: ', id);
      // await ApiUtil.deleteComment(id, this.$store.getters.username);
      // this.updateThread(this.cardProps.threadId);
    },
  },
};
</script>

<style lang="scss" scoped>
.comments-wrapper {
  text-align: start;
  max-width: 700px;
  margin: 0 auto;

  &__sub-comment {
    border: 1px solid rgb(224, 224, 224);
    padding: 10px;
    margin-left: 2rem;
    font-size: 14px;
  }
}
</style>
