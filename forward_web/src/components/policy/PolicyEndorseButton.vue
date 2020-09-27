<template>
  <b-button v-if="isLoading" disabled>Loading...</b-button>
  <div v-else-if="isPolitician">
    <b-button
      v-if="!politician.hasEndorsed"
      variant="primary"
      v-b-modal.modal-endorse
    >
      Endorse
    </b-button>
    <b-button v-else variant="success" disabled>
      You've endorsed this policy!
    </b-button>
    <b-modal
      ref="modal-endorse"
      id="modal-endorse"
      :title="policy.name"
      @shown="focusTextarea"
      centered
      no-close-on-backdrop
    >
      <b-form>
        <b-form-textarea
          class="comment-form__text-area"
          id="textarea-no-auto-shrink"
          placeholder="Write your stance on this policy"
          no-auto-shrink
          v-model="stanceText"
          ref="focusText"
        ></b-form-textarea>
      </b-form>
      <template v-slot:modal-footer>
        <b-button v-if="stanceText.length < 1" disabled>Submit</b-button>
        <b-button v-else-if="isSubmitting" disabled>
          <b-spinner small type="grow"></b-spinner>
          Submitting...
        </b-button>
        <b-button v-else variant="primary" @click="handleSubmit">
          Submit
        </b-button>
        <b-button variant="danger" @click="hideEndorseModal">
          Cancel
        </b-button>
      </template>
    </b-modal>
  </div>
</template>

<script>
import { ApiUtil } from '@/_utils/api-utils';
import { simulateApiCall } from '@/_utils/common-utils';

export default {
  props: {
    policy: Object,
  },
  data() {
    return {
      stanceText: '',
      isSubmitting: false,
      politician: {},
      isPolitician: false,
      isLoading: true,
    };
  },
  async created() {
    const user = this.$store.getters.userState;

    if (user.approved) {
      this.isPolitician = true;
      const modifiedPolitician = this.$store.getters.getPolitician;
      
      // use politician vuex store if available 
      if (modifiedPolitician.id) {
        this.politician = modifiedPolitician;
      } else {
        await this.$store.dispatch('setPolitician', user);
        this.politician = this.$store.getters.getPolitician;
      }

      const endorsedPolicies = this.politician.endorsed;
      for (const endorsed of endorsedPolicies) {
        if (endorsed.policy_id === this.policy.id) {
          this.politician.hasEndorsed = true;
          this.isLoading = false;
          return;
        }
      }
      this.politician.hasEndorsed = false;
    }
    this.isLoading = false;
  },
  methods: {
    async handleSubmit() {
      this.isSubmitting = true;
      try {
        await this.addNewStance();
        await this.updatePoliticianEndorsements();
        this.politician.hasEndorsed = true;
      } catch (error) {
        alert(error, 'On submitting stance');
      }
      this.isSubmitting = false;
      this.hideEndorseModal();
    },
    addNewStance() {
      const newStance = {
        policy_id: this.policy.id,
        politician_id: this.politician.id,
        content: this.stanceText,
      };
      return ApiUtil.postStance(newStance);
    },
    async updatePoliticianEndorsements() {
      const stances = await ApiUtil.getAllStances(this.politician.id);
      await this.$store.dispatch('updateEndorsed', stances);
    },
    hideEndorseModal() {
      this.$refs['modal-endorse'].hide();
      this.stanceText = '';
    },
    focusTextarea() {
      this.$refs.focusText.focus();
    },
  },
};
</script>

<style lang="scss" scoped></style>
