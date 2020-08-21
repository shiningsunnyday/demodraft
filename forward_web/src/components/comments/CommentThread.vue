<template>
  <div class="comments-wrapper__comment">
    <!-- Leading comment -->
    <CommentCard :comment="comment">
      <!-- Card buttons -->
      <template v-slot:buttons>
        <BButton v-if="hasReplies" @click="handleViewReplies(comment.thread_id)" variant="link">
          view replies
        </BButton>
        <BButton variant="link" @click="handleReplyClick"> reply </BButton>
        <BButton v-if="isMod" variant="link" @click="deleteThread(comment.thread_id)"> delete </BButton>
      </template>
      <!-- End card buttons -->

      <!-- Reply form -->
      <template v-slot:reply-form v-if="isReplying">
        <CommentForm
          :updateComments="updateRepliesView"
          :threadId="comment.thread_id"
          :isReply="true"
        ></CommentForm>
      </template>
      <!-- End reply form -->
    </CommentCard>
    <!-- End leading comment -->

    <!-- Replies to leading comment -->
    <div v-if="isViewReplies" v-for="(reply, index) in thread" :key="reply.id">
      <CommentCard
        :comment="reply"
        :className="`comments-wrapper__sub-comment`"
      >
        <template v-slot:buttons>
          <BButton v-if="isMod" variant="link" @click="deleteComment(index)"> delete </BButton>
        </template>
      </CommentCard>
    </div>
    <!-- End replies to leading comment -->
  </div>
</template>

<script>
import { BButton, BIcon, BIconHandThumbsUp } from 'bootstrap-vue';
import CommentCard from './CommentCard';
import CommentForm from "@/components/comments/CommentForm";
import { ApiUtil } from "@/_utils/api-utils.js";

export default {
  name: 'CommentThread',
  components: {
    'b-button': BButton,
    BIcon,
    BIconHandThumbsUp,
    CommentCard,
    CommentForm
  },
  props: {
    comment: Object,
    className: String,
    updateComments: Function,
  },
  data() {
    return {
      isViewReplies: false,
      hasReplies: false,
      thread: [],
      isReplying: false,
      isMod: true,
    };
  },
  async mounted () {
    const { comment } = this; // props
    this.thread = await ApiUtil.getThreadFromComment(comment.thread_id);
    this.hasReplies = this.thread.length > 0 ? true : false;
  },
  methods: {
    async handleViewReplies(threadId) {
      // prevent unecessary api calls when closing replies
      if (!this.isViewReplies) {
        this.thread = await ApiUtil.getThreadFromComment(threadId);
      }
      this.isViewReplies = !this.isViewReplies;
    },
    handleReplyClick() {
      this.isReplying = !this.isReplying;
    },
    async deleteThread(threadId) {
      await ApiUtil.deleteThread(threadId, this.$store.getters.username);
      this.updateComments();
    },
    async deleteComment(index) {
      let id;
      if (index == 0) {
        id = this.comment.id;
      } else {
        id = this.thread[index-1].id;
      }
      console.log(id);
      await ApiUtil.deleteComment(id, this.$store.getters.username);
      this.thread = await ApiUtil.getThreadFromComment(
        this.comment.thread_id
      );
    },
    async updateRepliesView() {
      this.thread = await ApiUtil.getThreadFromComment(
        this.comment.thread_id
      );
      // Only open replies if closed
      if (!this.isViewReplies) {
        this.isViewReplies = !this.isViewReplies;
      }
      this.hasReplies = true;
    }
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
