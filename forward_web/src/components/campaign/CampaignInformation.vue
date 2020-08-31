<template>
  <div class="campaign-info">
    <!-- <BForm>
      <BFormGroup id="first-group" label="First Name *" label-for="firstname">
        <BFormInput
          id="firstname"
          v-model="user.firstName"
          type="text"
          required
          disabled
        />
      </BFormGroup>

      <BFormGroup
        id="last-group"
        label="Last Name *"
        label-for="lastname"
      >
        <BFormInput 
          id="lastname" 
          v-model="user.lastName" 
          type="text" 
          required 
          disabled
        />
      </BFormGroup>

      <BFormGroup
        id="bio-group"
        label="Biography *"
        label-for="bio"
        description="You can change this later"
      >
        <b-form-textarea
          id="bio"
          v-model="user.bio" 
          rows="6"
          required
          disabled 
        >
        </b-form-textarea>
      </BFormGroup>

      <BFormGroup 
        id="website-group" 
        label="Website:" 
        label-for="website">
        <BFormInput
          id="website"
          v-model="user.website"
          type="text"
          disabled
        />
      </BFormGroup>

      <BFormGroup 
        id="actblue-group" 
        label="Actblue:" 
        label-for="actblue">
        <BFormInput
          id="actblue"
          v-model="user.actblue"
          type="text"
          disabled
        />
      </BFormGroup>

      <BFormGroup  
        prepend="$" 
        append=".00"
        id="fundraise-group" 
        label="Fundraising Goal:" 
        label-for="fundraise"
        description="* required fields"
      >
        <b-form-input
          id="fundraise"
          v-model="user.goal"
          type="number"
          min="0"
          max="5000"
          disabled
        />
      </BFormGroup > 
    <b-button 
      @click="handleSubmitCampaign" 
      class="campaign-info__launch-campaign"
    >
      Launch Campaign
    </b-button>
    </BForm>-->
    <div 
      v-if="isLaunching"
      class="campaign-info__button-group"
    >
      <b-button
        size="lg"
        class="campaign-info__launch-campaign"
        disabled
      >
        <b-spinner type="grow" label="Loading..."> </b-spinner>
        Launch Campaign Now!
      </b-button>
      <b-button disabled>
        Take me back!
      </b-button>
    </div>

    <div v-else class="campaign-info__button-group">
      <b-button
        @click="$emit('handleSubmitCampaign')"
        size="lg"
        variant="primary"
        class="campaign-info__launch-campaign"
      >
        Launch Campaign Now!
      </b-button>
      <b-button @click="$emit('handleBack')">
        Take me back!
      </b-button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CampaignInformation',
  props: {
    data: Object,
    isLaunching: Boolean,
  },
  data() {
    return {
      user: {
        firstName: '',
        lastName: '',
        bio: '',
        website: '',
        actblue: '',
        goal: '',
      },
    };
  },
};
</script>

<style lang="scss" scoped>
.campaign-info {
  // margin: 0 auto;
  // width: 700px;
  &__button-group {
    display: flex;
    flex-direction: column;
    
    :nth-child(2) {
      margin: 1em auto;
      padding: 8px;
      max-width: 150px;
    }
  }
}
</style>
