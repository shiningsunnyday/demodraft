<template>
  <div class="campaign-pending__status">
    <h4>
      Thank you for submitting a request to launch your campaign!
    </h4>
    <h4>
      You will be notified through email within 12-24 hours when your
      application is accepted.
    </h4>
    <h4>
      In the meantime, feel free to browse policies, politicians, and join the coversation!
    </h4>
  </div>
</template>

<script>
export default {
  name: 'CampaignPending',
};
</script>

<style lang="scss" scoped>
.campaign-pending {
  &__status {
    display: flex;
    flex-direction: column;
    justify-content: center;
    margin-top: 100px;
    text-align: center;

    h4 {
      margin-bottom: 20px;
      @media screen and (max-width: 1024px) {
        font-size: 18px;
      }
    }
  }
}
</style>
