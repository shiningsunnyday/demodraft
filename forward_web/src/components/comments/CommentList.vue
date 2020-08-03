<template>
  <div>
    <h1>Comments</h1>

    <div 
      class="comments-wrapper"
      v-if="comments.length" 
      v-for="(comment, index) in comments" 
      :key="`comment-${index}`"
    >
      <CommentThread :comment="comment"></CommentThread>
    </div>
  </div>
</template>

<script>
import { BButton, BIcon, BIconHandThumbsUp } from "bootstrap-vue";
import { ApiUtil } from "@/_utils/api-utils.js";
import CommentThread from './CommentThread';

export default {
  name: "CommentList",
  /** 
   * lets keep components at the top - underneath name:
   * so we know what components are being used right away
  */
  components: {
    "b-button": BButton,
    BIcon,
    BIconHandThumbsUp,
    CommentThread,
  },
  data() {
    return {
      comments: [],
      isViewReplies: false,
    };
  },
  /**
   * lets keep life cycles methods above standard methods
   * to more represent the order of events on component creation
   */
  async created() {
    this.comments= await ApiUtil.getPolicyComments(
      this.$route.params.id
    );
  },
};
</script>

<style lang="scss" scoped>
.comments-wrapper {
  text-align: start;
  max-width: 700px;
  margin: 0 auto;
}
</style>
