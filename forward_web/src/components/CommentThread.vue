<template>
  <div class="comments-wrapper__comment">
    <!-- Leading comment -->
    <CommentCard
      :comment="comment[0]"
      :className="`comments-wrapper__lead-comment`"
    >
      <BButton
        v-if="comment[1]"
        variant="link"
        @click="handleViewReplies(comment[0].id)"
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
import { ApiUtil } from '../_utils/api-utils';

export default {
  name: 'CommentThread',
  components: {
    'b-button': BButton,
    BIcon,
    BIconHandThumbsUp,
    CommentCard,
  },
  props: {
    comment: Array,
    className: String,
  },
  data() {
    return {
      isViewReplies: false,
      thread: [],
    };
  },
  methods: {
    async handleViewReplies(leadCommentId) {
      // prevent unecessary api calls when closing replies
      if (!this.isViewReplies) {
        console.log('fetch thread');
        this.thread = await ApiUtil.getThreadFromComment(leadCommentId);
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
    padding: 10px;
    margin-bottom: 10px;
  }

  &__lead-comment {
    border: 1px solid rgb(224, 224, 224);
  }

  &__sub-comment {
    border: 1px solid rgb(224, 224, 224);
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
