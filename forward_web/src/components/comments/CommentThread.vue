<template>
  <div class="comments-wrapper__comment">
    <!-- Leading comment -->
    <CommentCard :comment="comment" :className="`comments-wrapper__lead-comment`">
      <!-- Card buttons -->
      <template v-slot:buttons>
        <BButton v-if="hasReplies" @click="handleViewReplies(comment.thread_id)" variant="link">
          view replies
        </BButton>
        <BButton variant="link" @click="handleReplyClick"> reply </BButton>
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
    <div v-if="isViewReplies" v-for="replies in thread" :key="replies.id">
      <CommentCard
        :comment="replies"
        :className="`comments-wrapper__sub-comment`"
      ></CommentCard>
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
    async updateRepliesView() {
      this.thread = await ApiUtil.getThreadFromComment(
        this.comment.thread_id
      );
      // when replying, keep 'replies view' open if already opend
      // and to open 'replies view' if closed
      // this looks so dumb lmao
      if (!this.isViewReplies) {
        this.isViewReplies = !this.isViewReplies;
      }
      this.hasReplies = true;
    }
  },
};
</script>

<style lang="scss">
.comments-wrapper {
  text-align: start;
  max-width: 700px;
  margin: 0 auto;
  &__comment {
    margin-bottom: 8px;
  }

  &__lead-comment {
    padding: 10px;
    border: 1px solid rgb(224, 224, 224);
  }

  &__sub-comment {
    border: 1px solid rgb(224, 224, 224);
    padding: 10px;
    margin-left: 2rem;
  }

  &__child-comment {
    margin-left: 8px;
  }

  &__like {
    display: flex;
    align-items: center;
  }

  &__like-icon {
    margin: 8px;
    cursor: pointer;
    &:hover {
      fill: green;
    }
  }

  .btn {
    margin: 8px;
  }
}
</style>
