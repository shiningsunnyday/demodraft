<template>
  <BCard class="policy-card-container">
    <div class="card-content">
      <div class="card-title-wrapper">
        <b-card-title>
          {{ policy.name }}
        </b-card-title>
      </div>

      <hr />

      <div class="policy-statement line-clamp">
        <p>{{ policy.statement }}</p>
      </div>

      <div class="policy-card__flex-barrier">
        <b-button 
          variant="link" 
          @click="handleLearnMore"
          class="policy-card__learn-more"
        >
          Learn more
        </b-button>
      </div>

      <div class="policy-card__flex-barrier">
        <p class="policy-card__category-name">
          {{ policy.categoryName }}
        </p>
      </div>
      <hr />
    </div>
    <div class="card-data-container">
      <b-button
        class="like-btn-wrapper card-data-btn"
        variant="outline"
        @click="handlePolicyLike"
      >
        <BIconHandThumbsUp
          class="like-button"
          style="width: 25px; height: 25px;"
        />
        <span class="likes-counter">{{ policy.likes }}</span>
      </b-button>
    </div>
  </BCard>
</template>

<script>
import { ApiUtil } from '@/_utils/api-utils';
import { BIconHandThumbsUp } from 'bootstrap-vue';

export default {
  name: 'PolicyCard',
  components: {
    BIconHandThumbsUp,
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
    async handleLearnMore() {
      const pushedPolicy = await ApiUtil.getPolicy(this.policy.id);
      this.$router.push({
        name: 'selected-policy',
        params: {
          id: this.policy.id,
          isPushed: true,
          pushedPolicy: pushedPolicy,
        },
      });
    },
    async handlePolicyLike() {
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
@import '@/_styles';

.policy-card-container {
  width: 500px;
  height: 365px;
  margin: 20px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12), 0 1px 2px rgba(0, 0, 0, 0.24);

  // mobile
  @media screen and (max-width: 768px) {
    width: 300px;
    margin: 20px 5px;
  }

  .card-body {
    display: flex;
    flex-direction: column;
    margin: 0 auto;
    width: 450px;
    padding: 20px 0px 10px 0px;

    // mobile
    @media screen and (max-width: 768px) {
      display: flex;
      flex-direction: column;
      width: 275px;
    }

    .card-content {
      display: flex;
      flex-direction: column;
      padding: 10px 15px 0 15px;

      // mobile
      @media screen and (max-width: 768px) {
        padding: 10px 5px 0 5px;
      }

      .card-title-wrapper {
        height: 60px;
        display: flex;
        justify-content: center;
        align-items: center;

        .card-title {
          margin: 0;
          text-align: center;
          font-size: 1.2rem;
          font-weight: bold;
        }
      }

      .policy-statement {
        width: 350px;
        height: 75px;
        margin: 0 auto;
        text-align: center;
        overflow: hidden;

        // mobile
        @media screen and (max-width: 768px) {
          width: 245px;
        }
      }
      .policy-statement p {
        margin: 0;
      }

      // keeps the policy statement 3 lines long and adds ellipses to the end
      .line-clamp {
        display: -webkit-box;
        -webkit-line-clamp: 3;
        -webkit-box-orient: vertical;
      }

      hr {
        // border: 0;
        clear: both;
        display: block;
        width: 100%;
        background-color: lightgray;
        height: 1px;
      }
    }

    .card-data-container {
      display: flex;
      flex-direction: row;
      // justify-content: flex-end;
      padding: 0 15px;
      width: 100%;
      // margin-top: 10px;

      // mobile
      @media screen and (max-width: 768px) {
        padding: 0 5px;
      }

      .like-btn-wrapper {
        padding: 0;
        display: block;

        .likes-counter {
          margin-left: 3px;
        }
      }
    }
  }
}

.policy-card {

  &__learn-more{
    display: inline-block;
    margin-bottom: 8px;
  }

  &__category-name {
    display: inline-block;
    background: #2c3e50;
    color: white;
    padding: 3px 10px;
    margin: 0;
    border-radius: 5px;
    font-size: 12px;
    @media screen and (min-width: 768px) {
      font-size: 14px;
    }
  }
}
</style>
