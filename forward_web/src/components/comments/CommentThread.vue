<template>
  <div class="comments-wrapper__comment">
    <!-- Leading comment -->
    <CommentCard
      :comment="comment"
      :className="`comments-wrapper__lead-comment`"
    >
      <BButton
        v-if="hasReplies"
        @click="handleViewReplies(comment.thread_id)"
        variant="link"
      >
        view replies
      </BButton>
    </CommentCard>

    <!-- replies to leading comment -->
    <div v-if="isViewReplies" v-for="replies in thread" :key="replies.id">
      <CommentCard
        :comment="replies"
        :className="`comments-wrapper__sub-comment `"
      ></CommentCard>
    </div>
  </div>
</template>

<script>
import { BButton, BIcon, BIconHandThumbsUp } from 'bootstrap-vue';
import CommentCard from './CommentCard';
import { ApiUtil } from "@/_utils/api-utils.js";

export default {
  name: 'CommentThread',
  components: {
    'b-button': BButton,
    BIcon,
    BIconHandThumbsUp,
    CommentCard,
  },
  props: {
    comment: Object,
    className: String,
  },
  data() {
    return {
      isViewReplies: false,
      hasReplies: false,
      thread: [],
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
        //console.log('thread fetched');
      }
      this.isViewReplies = !this.isViewReplies;
    },
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
