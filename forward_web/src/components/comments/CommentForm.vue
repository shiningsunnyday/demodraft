<template>
  <div class="comment-form">
    <b-form @submit.prevent="handleSave">
      <b-form-textarea
        class="comment-form__text-area"
        id="textarea-no-auto-shrink"
        placeholder="Comment on this policy"
        rows="3"
        max-rows="8"
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
    handleNewThread: Function,
  },
  data() {
    return {
      text: '',
    };
  },
  methods: {
    async handleSave() {
      const data = {
        policy_id: this.policyId,
        username: this.$store.getters.username,
        content: this.text,
      };
      // adding new thread to database
      await ApiUtil.addNewThread(data);
      // updates comment section
      await this.handleNewThread();
      console.log(data);
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
