<template>
  <div class="comments-wrapper__lead-comment" :class="className">
    <p class="comments-wrapper__username">{{ comment.username }}</p>
    <p class="comments-wrapper__content">{{ comment.content }}</p>
    <div class="comments-wrapper__options">
      <div class="comments-wrapper__like">
        <BIconHandThumbsUp
          class="comments-wrapper__like-icon"
          variant="dark"
          v-on:click="handleClick(comment.id)"
        />
        <span v-if="!liked">{{ comment.likes }}</span>
        <span v-else>{{ likes }}</span>
      </div>
      <!-- view replies/reply buttons -->
      <slot name="buttons"></slot>
    </div>
    <slot name="reply-form"></slot>
  </div>
</template>

<script>
import { BButton, BIcon, BIconHandThumbsUp } from 'bootstrap-vue';
import { ApiUtil } from '@/_utils/api-utils.js';

export default {
  name: 'CommentCard',
  components: {
    BButton,
    BIcon,
    BIconHandThumbsUp,
  },
  props: {
    comment: Object,
    className: String,
  },
  data() {
    return {
      liked: false,
      likes: 0,
    };
  },
  methods: {
    // prevent hard spamming likes for now
    // will need to use Vuex state managment to handle this
    // specific user since you can refresh the page and like again
    async handleClick(id) {
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
