<template>
  <div class="about">
    <h1>Community Guidelines</h1>

    <h3>Maintain respect</h3>
    <p>
      Demodraft recognizes that disagreement is normal, but we are here to
      provide a safe place for discussion about policy, not about each other.
    </p>

    <h3>Be accurate</h3>
    <p>
      Making factual claims solely from speculation and without evidence is
      discouraged and will be under moderation.
    </p>

    <h3>Keep comments relevant</h3>
    <p>
      When commenting on policies or politicians, please keep your contributions
      on topic so as not to cause extra noise for other users.
    </p>

    <h3>Remember the Golden Rule</h3>
    <p>
      Most importantly, treat others as you would like to be treated --
      regardless of our backgrounds and viewpoints, we are all human and deserve
      respect, kindness, and consideration
    </p>
  </div>
</template>

<script>
export default {
  name: 'about-page',
};
</script>

<style lang="scss" scoped>
@import '@/_styles';

.about {
  padding: 0 20px;
  margin: 0 auto;
  text-align: center;

  @media screen and (min-width: 768px) {
    width: 800px;
  }

  h1 {
    font-weight: bold;
    margin-bottom: 3rem;
  }

  h3 {
    font-weight: bold;
  }

  p {
    margin-bottom: 50px;
    @include font-sizing;
  }
}
</style>
