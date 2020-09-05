<template>
  <div class="comments-wrapper__comment">
    <div v-if="isLoading">
      <CommentCardPlaceholder />
    </div>
    <div v-else>
      <!-- Leading comment -->
      <CommentCard
        :comment="leadComment"
        :prop="cardProps"
        :isLeadComment="true"
        @handleViewReplies="handleViewReplies"
        @updateRepliesView="updateRepliesView"
        @deleteThread="handleDeleteThread"
        @deleteComment="handleDeleteComment"
        class="comments-wrapper__lead-comment"
      ></CommentCard>
      <!-- End leading comment -->

      <!-- Replies to leading comment -->
      <div
        v-show="cardProps.isViewingReplies"
        v-for="(reply, index) in replies"
        :key="reply.id"
        class="reply-wrapper"
      >
        <div @click="handleBarClick" class="reply-wrapper__bar"></div>
        <CommentCard
          :comment="reply"
          :index="index"
          :prop="cardProps"
          @handleViewReplies="handleViewReplies"
          @updateRepliesView="updateRepliesView"
          @deleteThread="handleDeleteThread"
          @deleteComment="handleDeleteComment"
          :className="`reply-wrapper__comment`"
        ></CommentCard>
      </div>
      <b-button
        v-if="cardProps.isViewingReplies"
        @click="handleReplyToThread"
        variant="link"
      >
        reply to thread
      </b-button>
      <CommentFormReply
        v-if="isRepyThread"
        :updateComments="updateRepliesView"
        :threadId="comment.thread_id"
        :replyTo="comment"
      />
      <!-- End replies to leading comment -->
    </div>
  </div>
</template>

<script>
import CommentCard from './CommentCard';
import CommentCardPlaceholder from './CommentCardPlaceholder';
import CommentFormReply from '@/components/comments/CommentFormReply';
import { ApiUtil } from '@/_utils/api-utils.js';

export default {
  name: 'CommentThread',
  components: {
    CommentCard,
    CommentFormReply,
    CommentCardPlaceholder,
  },
  props: {
    comment: Object,
    className: String,
    updateComments: Function,
  },
  data() {
    return {
      replies: [], // might use stack datastructure
      replyComment: {}, // in progress
      isLoading: true,
      leadComment: this.comment,
      isRepyThread: false,
      cardProps: { // needs refactoring
        isViewingReplies: false,
        hasReplies: false,
        threadId: 0,
        isMod: false, // change this to true for testing
      },
    };
  },
  async created() {
    try {
      const thread = await ApiUtil.getThreadFromComment(this.comment.thread_id);
      this.cardProps.threadId = this.comment.thread_id;
      this.cardProps.hasReplies = thread.replies.length > 0;
      this.cardProps.isMod = this.$store.getters.getUserInfo.isMod;
      this.replies = thread.replies;
    } catch (error) {
      alert(error);
    }
    this.isLoading = false;
  },
  methods: {
    async updateThread(threadId) {
      const thread = await ApiUtil.getThreadFromComment(threadId);
      this.replies = thread.replies;
    },
    async handleAddReply() {
      const thread = await ApiUtil.getThreadFromComment(this.comment.thread_id);
      this.replies.push(thread.lastComment);
    },
    handleViewReplies(threadId) {
      // only make api call when viewing replies
      if (!this.cardProps.isViewingReplies) {
        this.updateThread(threadId);
      }
      this.cardProps.isViewingReplies = !this.cardProps.isViewingReplies;
    },
    updateRepliesView() {
      this.handleAddReply();
      const isRepliesOpen = this.cardProps.isViewingReplies;
      if (!isRepliesOpen) {
        const openReplies = !isRepliesOpen;
        this.cardProps.isViewingReplies = openReplies;
      }
      this.cardProps.hasReplies = true;
    },
    async handleDeleteThread(threadId) {
      try {
        await ApiUtil.deleteThread(threadId, this.$store.getters.username);
        this.updateComments();
      } catch (error) {
        alert(error.response);
        console.log(error);
      }
    },
    async handleDeleteComment(data) {
      const { index, comment } = data;
      const id = index === 0 ? this.comment.id : this.replies[index - 1].id;
      try {
        await ApiUtil.deleteComment(id, this.$store.getters.username);
        this.replies.pop();
      } catch (error) {
        alert(error.response);
        console.log(error);
      }
    },
    handleBarClick() {
      this.handleViewReplies();
    },
    handleReplyToThread() {
      this.isRepyThread = !this.isRepyThread;
    },
  },
};
</script>

<style lang="scss" scoped>
.comments-wrapper {
  text-align: start;
  max-width: 700px;
  margin: 0 auto;

  &__lead-comment {
    font-size: 14px;
    padding: 10px;
    border: 1px solid rgb(224, 224, 224);
    margin-bottom: 8px;
  }
}

.reply-wrapper {
  margin-bottom: 8px;
  position: relative;

  &__bar {
    content: '';
    width: 5px;
    height: calc(100% + 8px);
    background-color: grey;
    position: absolute;
    left: 1rem;
    top: -8px;
    &:hover {
      cursor: pointer;
    }
  }

  &__comment {
    border: 1px solid rgb(224, 224, 224);
    padding: 10px;
    margin-left: 2rem;
    font-size: 14px;
  }
}
</style>
