<template>
  <div class="about">
    <h3>Vision</h3>
    <p>
      Demodraft is empowering a new generation of politicians who reflect the
      communities they represent without influence from big money.
    </p>

    <h3>Mission</h3>
    <p>
      We are an incubator for normal people to “test the waters” before they
      officially declare candidacy. After their ideas achieve traction, we serve
      as a launchpad for their campaign run. We measure our success by the
      number of underdog victories we drive and the number of office incumbents
      we unseat.
    </p>

    <h3>People</h3>
    <p>
      On our platform, users can discover, fund, and support other users before
      they decide to run for office. They can let their ideas flourish through
      forums, polls and content, so those ideas can bring true change to our
      democracy.
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
    margin-bottom: 100px;
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
