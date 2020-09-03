<template>
  <LoadingSpinner v-if="isLoading"></LoadingSpinner>

  <b-container v-else class="policy">
    <h1 class="policy__title">{{ policy.name }}</h1>

    <div class="policy__content">
      <div class="policy__description-container">
        <p
          v-for="paragraph in description"
          :key="description.indexOf(paragraph)"
          class="policy__description"
        >
          {{ paragraph }}
        </p>
      </div>

      <hr />

      <div class="policy__btns-container">
        <b-button @click="likePolicy" class="policy__like" variant="outline">
          <BIconHandThumbsUp
            class="like-button"
            style="width: 25px; height: 25px;"
          />
          <span>{{ policy.likes }}</span>
        </b-button>

        <PolicyEndorseButton
          v-if="politician.approved"
          :politician="politician"
          :policy="policy"
        >
        </PolicyEndorseButton>
      </div>
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
import { BIconHandThumbsUp } from 'bootstrap-vue';

export default {
  name: 'selected-policy',
  components: {
    CommentList,
    CommentForm,
    PolicyEndorseButton,
    LoadingSpinner,
    BIconHandThumbsUp,
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
    window.scrollTo(0,0);
    
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
        this.hasLiked = true;
        this.policy.likes++;
        try {
          await ApiUtil.putPolicyLike(this.policy.id);
        } catch (error) {
          alert(error.message);
        }
      }
    },
  },
};
</script>

<style lang="scss" scoped>
@import '@/_styles';

.policy-loading {
  text-align: center;
}

.policy {
  text-align: center;
  height: 100%;
  margin-bottom: 5rem;

  &__title-and-likes {
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    max-width: 700px;
    margin: 0 auto;
  }

  &__title {
    font-weight: bold;
    margin-bottom: 25px;
  }

  &__description {
    text-align: left;
  }

  &__content {
    margin: 0 auto;
    max-width: 700px;
    @include font-sizing;
  }

  &__btns-container {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
  }
}
</style>
