<template>
  <LoadingSpinner v-if="isLoading"></LoadingSpinner>
  <b-container v-else class="policy">
    <h1 class="policy__title">{{ policy.name }}</h1>

    <b-button @click="likePolicy" class="policy__like">
      {{ `${policy.likes} like(s)` }}
    </b-button>

    <div class="policy__content">
      <!-- <h4 class="policy__statement">{{ policy.statement }}</h4> -->
      <p class="policy__description">{{ policy.description }}</p>
      <PolicyEndorseButton
        v-if="politician.approved"
        :politician="politician"
        :policy="policy"
      >
      </PolicyEndorseButton>
    </div>

    <hr />

    <CommentList :policyId="policy.id"></CommentList>
  </b-container>
</template>

<script>
import CommentList from '@/components/comments/CommentList';
import CommentForm from '@/components/comments/CommentForm';
import PolicyEndorseButton from '@/components/policy/PolicyEndorseButton';
import LoadingSpinner from '@/components/_common/LoadingSpinner';
import { ApiUtil } from '@/_utils/api-utils';

export default {
  name: 'selected-policy',
  components: {
    CommentList,
    CommentForm,
    PolicyEndorseButton,
    LoadingSpinner,
  },
  props: {
    pushedPolicy: Object,
    isPushed: Boolean,
  },
  data() {
    return {
      policy: {},
      politician: {},
      hasLiked: false,
      isLoading: true,
    };
  },
  async created() {
    console.log(this.isPushed);
    if (this.isPushed) {
      this.policy = this.pushedPolicy;
    } else {
      try {
        this.policy = await ApiUtil.getPolicy(this.$route.params.id);
      } catch (error) {
        alert(
          `Error ${error.response.status}: Something when wrong fetching this policy`
        );
        console.log(error);
      }
    }

    const user = this.$store.getters.getUserInfo;
    if (user.approved) {
      this.politician = await ApiUtil.getModifiedPolitician({ user });
      const endorsedPolicies = this.politician.endorsed;
      for (const endorsement of endorsedPolicies) {
        if (endorsement.policy_id === this.policy.id) {
          this.politician.hasEndorsed = true;
          break;
        }
      }
    }
    this.isLoading = false;
  },
  methods: {
    async likePolicy() {
      if (!this.hasLiked) {
        this.policy.likes = await ApiUtil.putPolicyLike(this.policy.id);
        this.hasLiked = true;
      }
    },
  },
};
</script>

<style lang="scss" scoped>
.policy-loading {
  text-align: center;
}

.policy {
  text-align: center;
  height: 100%;
  margin-bottom: 5rem;
  &__content {
    margin: 1rem 0;
  }

  &__description {
    text-align: justify;
  }
}
</style>
