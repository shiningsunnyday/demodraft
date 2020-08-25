<template>
  <div :class="className">
    <p v-if="highlightUser" class="comments-wrapper__comment-header --highlight">
      <span>{{ comment.username }}</span>
      <span>{{ timePosted }}</span>
    </p>
    <p v-else class="comments-wrapper__comment-header">
      <span>{{ comment.username }}</span>
      <span>{{ timePosted }}</span>
    </p>
    <p class="comments-wrapper__content">{{ comment.content }}</p>
    <div class="comments-wrapper__options">
      <div class="comments-wrapper__main-options">
        <div class="comments-wrapper__like">
          <BIconHandThumbsUp
            class="comments-wrapper__like-icon"
            v-on:click="handleLike(comment.id)"
          />
          <span v-if="!liked">{{ comment.likes }}</span>
          <span v-else>{{ likes }}</span>
        </div>
        <b-button @click="handleViewReplies" variant="link">
          {{ viewRepliesText }}
        </b-button>
        <b-button @click="toggleReplyClick" variant="link">
          {{ replyText }}
        </b-button>
      </div>
      <div v-if="prop.isMod" class="comments-wrapper__delete">
        <b-button 
          v-if="!isChildComment"
          @click="deleteThread" variant="link"
        >
          delete
        </b-button>
        <b-button 
          v-else
          @click="deleteComment" 
          variant="link"
        >
          delete
        </b-button>
      </div>
    </div>
    <CommentForm
      v-if="isReplying"
      :updateComments="updateRepliesView"
      :threadId="prop.threadId"
      :replyTo="comment"
      :isReply="true"
    ></CommentForm>
  </div>
</template>

<script>
import { BIconHandThumbsUp } from 'bootstrap-vue';
import { ApiUtil } from '@/_utils/api-utils.js';
import CommentForm from '@/components/comments/CommentForm';
import moment from 'moment';

export default {
  name: 'CommentCard',
  components: {
    BIconHandThumbsUp,
    CommentForm,
  },
  props: {
    comment: Object,
    index: Number,
    className: String,
    prop: {
      isViewingReplies: Boolean,
      hasReplies: Boolean,
      threadId: Number,
      isMod: Boolean,
    },
    isLeadComment: Boolean,
  },
  data() {
    return {
      liked: false,
      likes: 0,
      isChildComment: false,
      isReplying: false,
      highlightUser: false,
      isLastReply: false,
    };
  },
  created() {
    const { next_comment_id, id} = this.comment;
    this.isChildComment = next_comment_id ? true : false;
    this.isLastReply = id === next_comment_id;

    if (this.comment.username === this.$store.getters.username) {
      this.highlightUser = true;
    }
  },
  computed: {
    replyText() {
      if (this.isLeadComment) {
        return 'reply';
      }
    },
    viewRepliesText() {
      const { isChildComment } = this;
      const { hasReplies, isViewingReplies } = this.prop;

      if (!isViewingReplies && hasReplies) {
        return 'view replies';
      } 

      if (isViewingReplies && !isChildComment) {
        return 'hide replies';
      }
    },
    timePosted() {
      const { time } = this.comment;
      return moment(time).format('MM-DD-YYYY, hh:mmA');
    }
  },
  methods: {
    handleViewReplies() {
      this.$emit('handleViewReplies', this.prop.threadId);
    },
    toggleReplyClick() {
      this.isReplying = !this.isReplying;
    },
    async updateRepliesView() {
      this.$emit('updateRepliesView');
      this.isReplying = !this.isReplying;
    },
    deleteThread() {
      this.$emit('deleteThread', this.prop.threadId);
    },
    deleteComment() {
      const data = {
        index: this.index,
        comment: this.comment,
      };

      this.$emit('deleteComment', data);
    },
    async handleLike(id) {
      // prevent hard spamming likes for now
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
  
  &__comment-header {
    display: flex;
    justify-content: space-between;
    padding: 8px;
    background: #627b9c;
    color: white;
  }

  &__options {
    display: flex;
    justify-content: space-between;
    align-items: center;
    .btn {
      margin-left: 8px;
      font-size: 11px;
      font-weight: bold;
      padding: 0;
    }

    .btn:focus {
      box-shadow: none;
    }
  }

  &__main-options {
    display: flex;
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
  
  .--highlight {
    background: #1C94DC;
  }
}
</style>
