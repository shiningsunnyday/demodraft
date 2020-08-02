<template>
  <!-- Leading comment -->
  <div class="comments-wrapper__comment comments-wrapper__lead-comment">
    <p class="comments-wrapper__username">{{ comment[0].username }}</p>
    <p class="comments-wrapper__content">{{ comment[0].content }}</p>
    <div class="comments-wrapper__like">
      <BIconHandThumbsUp class="comments-wrapper__like-icon" variant="dark" />
      <span>{{ comment[0].likes }}</span>
      <BButton 
        v-if="comment[1]"
        variant="link" 
        @click="handleViewReplies"
      >
        view replies
      </BButton>
    </div>
    
    <!-- replies to leading comment -->
    <div v-if="isViewReplies" v-for="replies in comment[1]" :key="replies.id">
      <div class="comments-wrapper__comment comments-wrapper__sub-comment">
        <p class="comments-wrapper__username">{{ replies.username }}</p>
        <p class="comments-wrapper__content">{{ replies.content }}</p>
        <div class="comments-wrapper__like">
          <BIconHandThumbsUp
            class="comments-wrapper__like-icon"
            variant="dark"
          />
          <span>{{ replies.likes }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { BButton, BIcon, BIconHandThumbsUp } from 'bootstrap-vue';

export default {
  name: 'CommentThread',
  components: {
    'b-button': BButton,
    BIcon,
    BIconHandThumbsUp,
  },
  data() {
    return {
      isViewReplies: false,
    };
  },
  props: {
    comment: Array,
    className: String,
    isLeadComment: true,
  },
  methods: {
    handleViewReplies() {
      this.isViewReplies = !this.isViewReplies;
    },
  },
};
</script>

<style lang="scss" scoped>
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
  }

  .btn {
    margin: 8px;
  }
}
</style>
