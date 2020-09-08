<template>
  <div class="campaign-pending__status">
    <h4>
      Thank you for submitting a request to launch your campaign!
    </h4>
    <!-- <br /> -->
    <h4>You will be notified when your application is accepted.</h4>
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
    }
  }
}
</style>
