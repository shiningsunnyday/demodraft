<template>
  <div>
    <h1>Comments</h1>

    <div 
      class="comments-wrapper"
      v-if="allComments.length" 
      v-for="(comment, index) in allComments" 
      :key="`comment-${index}`"
    >
      <CommentThread :comment="comment"></CommentThread>
    </div>
  </div>
</template>

<script>
import { BButton, BIcon, BIconHandThumbsUp } from "bootstrap-vue";
import { ApiUtil } from "../_utils/api-utils";
import CommentThread from './CommentThread';
// 1. Get list of comments linked to selected PolicyPage's id
// 2. For each comment that exists, created a CommentCard component
// 3. Render each of those CommentCard components

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
      allComments:[], // this should only take in lead comments (fix later)
      isViewReplies: false,
    };
  },
  /**
   * lets move life cycles above methods
   * to more represent the order of events on component creation
   */
  async created() {
    const { comments, allComments } = this;
    // *** Squashing all policy comments into a single array because it's easier to work with at the moment (need help understanding thread data structure better) ***
    const policyComments = await ApiUtil.getPolicyComments(
      this.$route.params.id
    );

    /**
     * Very convoluted way of storing comments at the moment.
     * Will need to see if there is a more efficient way of 
     * structuring leading comments and replies to those leading comments
     * 
     * for now this would look like:
     * [
     *  [{leading comment}, [array of replies to leading comment]]
     *  ie: [{}, [{},{},{},{}}]
     * ]
     */
    policyComments.forEach((currArr) => {
      let thread = [];
      let subComments = [];
      currArr.forEach((currComm, index) => {
        if (index === 0) {
          thread.push(currComm);
          return;
        } 

        if (currComm.id === currComm.next_comment_id) {
          subComments.push(currComm);
          thread.push(subComments);
          return;
        }

        subComments.push(currComm);
      });
      
      allComments.push(thread);
    });

    //console.log(allComments);
  },
  methods: {
    handleViewReplies() {
      this.isViewReplies = !this.isViewReplies;
      console.log("clicked");
    }
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
