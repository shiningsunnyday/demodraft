<template>
  <LoadingSpinner v-if="isLoading"></LoadingSpinner>
  <b-container v-else class="policy">
    <h1 class="policy__title">{{ policy.name }}</h1>

    <b-button @click="likePolicy" class="policy__like">
      {{ `${policy.likes} like(s)` }}
    </b-button>

    <div class="policy__content">
      <div class="policy__description-container">
        <p v-for="paragraph in description" class="policy__description">
          {{ paragraph }}
        </p>
      </div>
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
import { splitDescription } from '@/_utils/common-utils.js';

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
      description: '',
    };
  },
  async created() {
    try {
      if (this.isPushed) {
        this.policy = this.pushedPolicy;
      } else {
        this.policy = await ApiUtil.getPolicy(this.$route.params.id);
      }
    } catch (error) {
      alert(`Error ${error.response.status}: On fetching policy`);
      console.log(error);
    }

    this.description = splitDescription(this.policy.description);

    // test this on mounted()
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
      // will need database to keep track of likes
      if (!this.hasLiked) {
        this.policy.likes++;
        try {
          await ApiUtil.putPolicyLike(this.policy.id);
        } catch (error) {
          alert(error.message);
        }
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

  &__like {
    margin: 1em;
  }

  &__content {
    margin: 0 auto;
    max-width: 700px;
  }

  &__description {
    text-align: justify;
  }
}
</style>
