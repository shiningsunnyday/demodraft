<template>
  <div class="campaign-progress">
    <span :class="inputAdress">Input Address</span>
    <span :class="choosePosition">Choose Position</span>
    <!-- TODO change 'Launch Campaign' to 'Your information' when
    backend is able to receive use data -->
    <span :class="yourInformation">Launch Campaign</span>
  </div>
</template>

<script>
export default {
  name: 'CampaignProgressBar',
  props: {
    currentStep: Number,
  },
  computed: {
    inputAdress() {
      if (this.currentStep === 0) {
        return 'current';
      }

      if (this.currentStep > 0) {
        return 'complete';
      }
    },
    choosePosition() {
      if (this.currentStep === 1) {
        return 'current';
      }

      if (this.currentStep > 1) {
        return 'complete';
      }
    },
    yourInformation() {
      if (this.currentStep === 2) {
        return 'current';
      }
    }
  },
};
</script>

<style lang="scss" scoped>
.campaign-progress {
  display: flex;
  flex-direction: row;
  margin: 2rem 0;
  background-color: transparent;
  font-size: 14px;

  & > span {
    text-align: center;
    width: 100%;
    position: relative;
    color: rgb(200, 200, 200);
  }

  & > span::before {
    content: '';
    display: block;
    width: 15px;
    height: 15px;
    border: 3px solid rgb(200, 200, 200);
    border-radius: 50%;
    text-align: center;
    margin: 0 auto 5px auto;
    background-color: #edf4f1;
  }

  & > span::after {
    content: '';
    position: absolute;
    width: 100%;
    height: 2px;
    background-color: rgb(200, 200, 200);
    top: 7px; /* half of circle height */
    left: -50%;
    z-index: -1;
  }

  & > span:first-child::after {
    content: none;
  }

  & > span.current {
    color: #1C94DC;
    font-weight: bold;
  }

  & > span.current::before {
    background-color: #1C94DC;
    line-height: 15px;
  }

  & > span.complete {
    color: rgb(200, 200, 200);
  }

  & > span.complete::before {
    background-color: #1C94DC;
  }

  & > span.complete + span::after {
    background-color: #1C94DC;
  }

  @media screen and (max-width: 425px) {
    font-size: 11px;
  }
}
</style>
