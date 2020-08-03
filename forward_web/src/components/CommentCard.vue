<template>
  <div class="comments-wrapper__comment" :class="className">
    <p class="comments-wrapper__username">{{ comment.username }}</p>
    <p class="comments-wrapper__content">{{ comment.content }}</p>
    <div class="comments-wrapper__like">
      <BIconHandThumbsUp
        class="comments-wrapper__like-icon"
        variant="dark"
        v-on:click="handleClick(comment.id)"
      />
      <span v-if="!liked">{{ comment.likes }}</span>
      <span v-else>{{ likes }}</span>
      <slot></slot>
    </div>
  </div>
  </div>
</template>

<script>
import { BIcon, BIconHandThumbsUp } from 'bootstrap-vue';
import { ApiUtil } from '../_utils/api-utils';

export default {
  name: 'CommentCard',
  components: {
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
</style>
