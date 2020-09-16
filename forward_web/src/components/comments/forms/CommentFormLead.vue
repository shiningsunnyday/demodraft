<template>
  <div class="comment-form">
    <b-form @submit.prevent="handleSave">
      <b-form-textarea
        class="comment-form__text-area"
        id="textarea-no-auto-shrink"
        rows="3"
        max-rows="8"
        placeholder="Join the conversation"
        no-auto-shrink
        v-model="text"
      ></b-form-textarea>
      <b-button v-if="this.text.length < 1" disabled>Comment</b-button>
      <b-button v-else type="submit" variant="primary">Comment</b-button>
    </b-form>
  </div>
</template>

<script>
import { ApiUtil } from "@/_utils/api-utils";

export default {
  name: 'CommentFormLead',
  props: {
    commentFormId: Number,
    commentSection: String,
    updateComments: Function,
  },
  data() {
    return {
      text: '',
    };
  },
  methods: {
    async handleSave() {
      const { commentFormId, commentSection } = this;
      const username = this.$store.getters.username;
      switch (commentSection) {
      case 'policy':
        await ApiUtil.addNewThread({
          policy_id: commentFormId,
          username: username,
          content: this.text,
        });
        break;
      case 'politician':
        await ApiUtil.addNewThread({
          politician_id: commentFormId,
          username: username,
          content: this.text,
        });
        break;
      default: 
        alert('Non specified comment section');
        break;
      }
      this.updateComments();
      this.text = '';
    },
  },
};
</script>

<style lang="scss" scoped>
.comment-form {
  text-align: start;
  max-width: 700px;
  margin: 1rem auto;

  &__text-area {
    margin: 10px 0;
  }
}
</style>
