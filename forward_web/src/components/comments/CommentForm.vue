<template>
  <div class="comment-form">
    <b-form @submit.prevent="handleSave">
      <b-form-textarea
        v-if="isReply"
        class="comment-form__text-area"
        id="textarea-no-auto-shrink"
        rows="3"
        max-rows="8"
        placeholder="Reply to OP of the thread (reply to user in progress)"
        no-auto-shrink
        v-model="text"
      ></b-form-textarea>
      <b-form-textarea
        v-else
        class="comment-form__text-area"
        id="textarea-no-auto-shrink"
        rows="3"
        max-rows="8"
        placeholder="Comment on this policy"
        no-auto-shrink
        v-model="text"
      ></b-form-textarea>
      <b-button v-if="this.text.length < 1" disabled>save</b-button>
      <b-button v-else type="submit" variant="primary">save</b-button>
    </b-form>
  </div>
</template>

<script>
import { ApiUtil } from "@/_utils/api-utils";

export default {
  name: 'CommentForm',
  props: {
    policyId: Number,
    threadId: Number,
    updateComments: Function,
    isReply: Boolean,
    replyTo: Object
  },
  data() {
    return {
      text: '',
    };
  },
  methods: {
    async handleSave() {
      if (this.isReply) {
        const user = {
          threadId: this.threadId,
          content: this.text
        };
        
        const replyToUser = {
          id: this.replyTo.id,
          username: this.replyTo.username,
          content: this.replyTo.content,
          threadId: this.threadId
        };
        
        console.log('user: ', user);
        console.log('reply to:', replyToUser);

        await ApiUtil.addNewReply({
          thread_id: this.threadId,
          username: this.$store.getters.username,
          content: this.text,
        });
      } else {
        await ApiUtil.addNewThread({
          policy_id: this.policyId,
          username: this.$store.getters.username,
          content: this.text,
        });
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
