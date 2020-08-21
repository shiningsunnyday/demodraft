<template>
  <div class="comments-wrapper__comment">
    <div v-if="isLoading">
      <CommentCardPlaceholder />
    </div>
    <div v-else>
      <!-- Leading comment -->
      <CommentCard
        :comment="comment"
        :status="status"
        :threadId="threadId"
        @handleViewReplies="handleViewReplies"
        @updateRepliesView="updateRepliesView"
      ></CommentCard>
      <!-- End leading comment -->

      <!-- Replies to leading comment -->
      <div v-if="status.isViewingReplies" v-for="reply in replies" :key="reply.id">
        <CommentCard
          :comment="reply"
          :threadId="threadId"
          :status="status"
          @handleViewReplies="handleViewReplies"
          @updateRepliesView="updateRepliesView"
          :className="`comments-wrapper__sub-comment`"
        ></CommentCard>
      </div>
      <!-- End replies to leading comment -->
    </div>
  </div>
</template>

<script>
import { BButton, BIcon, BIconHandThumbsUp } from 'bootstrap-vue';
import CommentCard from './CommentCard';
import CommentCardPlaceholder from './CommentCardPlaceholder';
import CommentForm from '@/components/comments/CommentForm';
import { ApiUtil } from '@/_utils/api-utils.js';

export default {
  name: 'CommentThread',
  components: {
    'b-button': BButton,
    BIcon,
    BIconHandThumbsUp,
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
      threadId: 0,
      replies: [],
      status: {
        isViewingReplies: false,
        hasReplies: false,
      },
      replyComment: {}, // in progress
      isLoading: true,
    };
  },
  async created() {
    this.threadId = this.comment.thread_id;
    const thread = await ApiUtil.getThreadFromComment(this.threadId);
    this.replies = thread.replies;
    this.status.hasReplies = this.replies.length > 0 ? true : false;
    this.isLoading = false;
  },
  methods: {
    async updateThread(threadId) {
      const thread = await ApiUtil.getThreadFromComment(threadId);
      this.replies = thread.replies;
    },
    handleViewReplies(threadId) {
      // only make api call when viewing replies
      if (!this.status.isViewingReplies) {
        this.updateThread(threadId);
      }
      this.status.isViewingReplies = !this.status.isViewingReplies;
    },
    updateRepliesView() {
      this.updateThread(this.threadId);
      // only open replies if closed
      if (!this.status.isViewingReplies) { 
        this.status.isViewingReplies = !this.status.isViewingReplies;
      }
      this.status.hasReplies = true;
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
  }
}
</style>
