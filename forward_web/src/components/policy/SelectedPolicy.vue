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

        <PolicyEndorseButton :policy="policy" />
      </div>
    </div>

    <hr />

    <Comments 
      :commentFormId="policy.id"
      :commentSection="'policy'" 
    />
    
  </b-container>
</template>

<script>
import Comments from '@/components/comments/Comments';
import PolicyEndorseButton from '@/components/policy/PolicyEndorseButton';
import { ApiUtil } from '@/_utils/api-utils';
import { splitDescription } from '@/_utils/common-utils.js';
import { BIconHandThumbsUp } from 'bootstrap-vue';

export default {
  name: 'selected-policy',
  components: {
    Comments,
    PolicyEndorseButton,
    BIconHandThumbsUp,
  },
  props: {
    pushedPolicy: Object,
    isPushed: Boolean,
  },
  data() {
    return {
      policy: {},
      hasLiked: false,
      isLoading: true,
      description: '',
    };
  },
  async created() {
    window.scrollTo(0,0);
    try {
      // isPushed = true when a user clicks on PolicyCard
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
    this.isLoading = false;
  },
  methods: {
    async likePolicy() {
      try {
        const username = this.$store.getters.username;
        const response = await ApiUtil.putPolicyLike({
          id: this.policy.id,
          username: username
        });
        if (response) {
          this.policy.likes++;
        }
      } catch (error) {
        console.log(error.response.status);
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
