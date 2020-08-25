<template>
  <BCard class="policy-card-container">
    <div class="policy-icon">
      <BIconCircleSquare style="width: 30px; height: 30px;" />
    </div>

    <div class="card-content">
      <b-card-title>
        {{ policy.name }}
      </b-card-title>

      <hr />

      <div class="module line-clamp">
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

    <div class="like-and-modal">
      <b-button variant="outline" @click="handlePolicyLike">
        <BIconHandThumbsUp
          class="like-button"
          style="width: 25px; height: 25px;"
        />
        <span>{{ policy.likes }}</span>
      </b-button>

      <b-button variant="outline">
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
  width: 300px;
  height: 300px;
  margin: 20px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);

  @media screen and (min-width: 768px) {
    width: 500px;
  }

  .card-body {
    @media screen and (min-width: 768px) {
      display: flex;
      flex-direction: row;
      justify-content: space-evenly;
      // padding: 15px 10px;
    }

    .card-content {
      @media screen and (min-width: 768px) {
        display: flex;
        flex-direction: column;
        flex-wrap: wrap;
        width: 350px;
        padding: 0 15px;
      }

      .module {
        width: 250px;
        margin: 0 auto;
        text-align: center;
        overflow: hidden;
      }
      .module p {
        margin: 0;
      }

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

      .card-title {
        font-size: 1.2rem;
        font-weight: bold;
      }
    }

    .like-and-modal {
      @media screen and (min-width: 768px) {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        padding-top: 2px;

        .btn {
          padding: 0;
        }

        .like-button {
          display: block;
        }

        .modal-button {
          display: block;
        }
      }
    }

    .like-button {
      display: none;
    }

    .modal-button {
      display: none;
    }
  }
}
</style>
