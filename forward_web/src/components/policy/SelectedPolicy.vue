<template>
  <b-container class="policy">
    <h1 class="policy__title">{{ policy.name }}</h1>
    <b-button @click="likePolicy" class="policy__like">
      {{ `${policy.likes} like(s)` }}
    </b-button>
    <div class="policy__content">
      <h4 class="policy__statement">{{ policy.statement }}</h4>
      <p class="policy__description">{{ policy.description }}</p>
      <PolicyEndorseButton :policy="policy"></PolicyEndorseButton>
    </div>
    <hr />
    <CommentList :policyId="policy.id"></CommentList>
  </b-container>
</template>

<script>
import CommentList from '@/components/comments/CommentList';
import CommentForm from '@/components/comments/CommentForm';
import PolicyEndorseButton from '@/components/policy/PolicyEndorseButton';
import { ApiUtil } from '@/_utils/api-utils';

export default {
  name: 'selected-policy',
  components: {
    CommentList,
    CommentForm,
    PolicyEndorseButton,
  },
  props: {
    policy: Object,
  },
  data() {
    return {
      hasLiked: false,
    };
  },
  methods: {
    async likePolicy() {
      if (!this.hasLiked) {
        this.likes = await ApiUtil.policyLike(this.$route.params.id);
        this.hasLiked = true;
      }
    },
  },
};
</script>

<style lang="scss" scoped>
.policy {
  text-align: center;

  &__content {
    margin: 1rem 0;
  }
}
</style>
