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
        <p>
          {{ policy.statement }}
        </p>
      </div>

      <b-button variant="link" @click="handleLearnMore">
        Learn more
      </b-button>

      <b-card-text class="policy__category">
        Category: {{ policy.category }}
      </b-card-text>
    </div>

    <div class="card-data-container">
      <div class="policy-icon card-data-btn">
        <BIconCircleSquare style="width: 27px; height: 27px;" />
      </div>

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

      <b-button class="modal-btn-wrapper" variant="outline">
        <BIconThreeDots
          class="modal-button"
          style="width: 25px; height: 25px;"
        />
      </b-button>
    </div>
  </BCard>
</template>

<script>
import { ApiUtil } from '@/_utils/api-utils';
import {
  BIconCircleSquare,
  BIconHandThumbsUp,
  BIconThreeDots,
} from 'bootstrap-vue';

export default {
  name: 'PolicyCard',
  components: {
    BIconCircleSquare,
    BIconHandThumbsUp,
    BIconThreeDots,
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
      if (!this.hasLiked) {
        try {
          this.policy.likes = await ApiUtil.putPolicyLike(this.policy.id);
          this.hasLiked = true;
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

.policy-card-container {
  width: 500px;
  height: 365px;
  margin: 20px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12), 0 1px 2px rgba(0, 0, 0, 0.24);

  // mobile
  @media screen and (max-width: 768px) {
    width: 300px;
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
      padding: 10px 15px;

      // mobile
      @media screen and (max-width: 768px) {
        padding: 10px 5px;
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
      padding: 0 15px;
      width: 100%;
      margin-top: auto;

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

      .modal-btn-wrapper {
        padding: 0;
        display: block;
        margin-left: auto;
        margin-right: 0;

        // mobile
        @media screen and (max-width: 768px) {
          display: none;
        }
      }

      .card-data-btn {
        margin-right: 20px;
      }
    }
  }
}
</style>
