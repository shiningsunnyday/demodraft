<template>
  <BCard class="policy-card" no-body>
    <div class="policy-card__card-content">
      <div class="policy-card__card-title-wrapper">
        <b-button @click="handleLearnMore" class="card-title" variant="link">
          {{ policy.name }}
        </b-button>
      </div>

      <hr />

      <div class="policy-card__policy-statement line-clamp">
        <p>{{ policy.statement }}</p>
      </div>

      <!-- <div class="policy-card__flex-barrier">
        <b-button
          variant="link"
          @click="handleLearnMore"
          class="policy-card__learn-more"
        >
          Learn more
        </b-button>
      </div> -->

      <hr />
    </div>

    <div class="policy-card__data-container">
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
      <div class="policy-card__flex-barrier">
        <p class="policy-card__category-name">
          {{ policy.categoryName }}
        </p>
      </div>
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

@mixin tablet-media-query {
  @media screen and (min-width: $tablet-breakpoint) {
    @content;
  }
}

@mixin desktop-media-query {
  @media screen and (min-width: $desktop-breakpoint) {
    @content;
  }
}

@mixin desktop-xl-media-query {
  @media screen and (min-width: $desktop-xl-breakpoint) {
    @content;
  }
}

.policy-card {
  max-width: 950px;
  width: 100%;
  height: 365px;
  margin: 15px 10px;
  padding: 55px 15px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12), 0 1px 2px rgba(0, 0, 0, 0.24);

  @include tablet-media-query {
    width: 225px;
  }

  @include desktop-media-query {
    width: 300px;
    margin: 20px 10px;
  }

  @include desktop-xl-media-query {
    width: 450px;
  }

  // keeps the policy statement 3 lines long and adds ellipses to the end
  .line-clamp {
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }

  &__card-content {
    hr {
      clear: both;
      display: block;
      width: 100%;
      background-color: lightgray;
      height: 1px;
    }
  }

  &__card-title-wrapper {
    height: 60px;
    display: flex;
    justify-content: center;
    align-items: center;

    .card-title {
      margin: 0;
      padding: 0;
      text-align: center;
      font-size: 1.3rem;
      font-weight: bold;
    }
  }

  &__policy-statement {
    width: 245px;
    height: 75px;
    margin: 0 auto;
    text-align: center;
    overflow: hidden;

    p {
      margin: 0;
    }

    @include tablet-media-query {
      width: 185px;
    }

    @include desktop-media-query {
      width: 250px;
    }

    @include desktop-xl-media-query {
      width: 400px;
      margin: 20px 10px;
    }
  }

  &__learn-more {
    display: inline-block;
    margin-bottom: 8px;
    font-weight: bold;
  }

  &__data-container {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    padding: 0 2px;
    width: 100%;

    .like-btn-wrapper {
      padding: 0;
      display: block;

      .likes-counter {
        margin-left: 3px;
      }
    }
  }

  &__category-name {
    display: inline-block;
    background: #eeeeee;
    color: black;
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
