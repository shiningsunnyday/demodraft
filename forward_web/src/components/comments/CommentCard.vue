<template>
  <div class="comments-wrapper__lead-comment" :class="className">
    <p class="comments-wrapper__username">{{ comment.username }}</p>
    <p class="comments-wrapper__content">{{ comment.content }}</p>
    <div class="comments-wrapper__options">
      <div class="comments-wrapper__like">
        <BIconHandThumbsUp
          class="comments-wrapper__like-icon"
          variant="dark"
          v-on:click="handleLike(comment.id)"
        />
        <span v-if="!liked">{{ comment.likes }}</span>
        <span v-else>{{ likes }}</span>
      </div>
      <b-button 
        v-if="status.hasReplies && !status.isViewingReplies" 
        @click="handleViewReplies"
        variant="link"
      >
        view replies
      </b-button>
      
      <b-button 
        v-else-if="status.isViewingReplies && !isChildComment" 
        @click="handleViewReplies"
        variant="link"
      >
        hide replies
      </b-button>
      <b-button 
        v-else 
        @click="handleViewReplies"
        variant="link"
      >
        collapse thread
      </b-button>

      <b-button 
        v-if="isChildComment"
        @click="toggleReplyClick"
        variant="link"
      >
        reply to thread
      </b-button>
      <b-button 
        v-else
        @click="toggleReplyClick"
        variant="link"
      >
        reply
      </b-button>
    </div>
    <CommentForm
      v-if="isReplying"
      :updateComments="updateRepliesView"
      :threadId="threadId"
      :isReply="true"
    ></CommentForm>
  </div>
</template>

<script>
import { BIconHandThumbsUp } from 'bootstrap-vue';
import { ApiUtil } from '@/_utils/api-utils.js';
import CommentForm from "@/components/comments/CommentForm";

export default {
  name: 'CommentCard',
  components: {
    BIconHandThumbsUp,
    CommentForm
  },
  props: {
    comment: Object,
    threadId: Number,
    className: String,
    status: {
      isViewingReplies: Boolean,
      hasReplies: Boolean,
    }
  },
  data() {
    return {
      liked: false,
      likes: 0,
      commentTime: '',
      isChildComment: false,
      isReplying: false,
    };
  },
  created() {
    const time = this.comment.time;
    if (this.comment.next_comment_id) {
      this.isChildComment = true;
    }
  },
  methods: {
    handleViewReplies() {
      this.$emit('handleViewReplies', this.threadId);
    },
    toggleReplyClick() {
      console.log(this.comment);
      this.isReplying = !this.isReplying;
    },
    updateRepliesView() {
      this.$emit('updateRepliesView', this.comment);
    },
    async handleLike(id) { // prevent hard spamming likes for now
      if (!this.liked) {
        this.likes = await ApiUtil.commentLike(id);
        this.liked = true;
      }
    },
  },
};
</script>

<style lang="scss" scoped>
.comments-wrapper {
  &__lead-comment {
    padding: 10px;
    border: 1px solid rgb(224, 224, 224);
    margin-bottom: 8px;
  }

  &__username {
    padding: 8px;
    background: #627B9C;
    font-weight: bold;
    color: white;
  }

  &__options {
    display: flex;

    .btn {
      margin-left: 8px;
      font-size: 12px;
      font-weight: bold;
      padding: 0;
    }

    .btn:focus {
      box-shadow: none;
    }
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
}
</style>
