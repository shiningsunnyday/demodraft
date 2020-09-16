<template>
  <div>
    <div>
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
  </div>
</template>

<script>
import { ApiUtil } from '@/_utils/api-utils';
import { simulateApiCall } from '@/_utils/common-utils';

export default {
  props: {
    policy: Object,
    politician: Object,
  },
  data() {
    return {
      stanceText: '',
      isSubmitting: false,
    };
  },
  methods: {
    async handleSubmit() {
      this.isSubmitting = true;
      try {
        await this.addNewStance();
        await this.updatePoliticianEndorsements();
        this.politician.hasEndorsed = true;
      } catch (error) {
        alert('Oops, something went wrong submitting your stance.');
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
