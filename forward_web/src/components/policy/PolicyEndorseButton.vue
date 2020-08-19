<template>
  <div>
    <div>
      <b-button v-if="!politician.hasEndorsed" variant="primary" v-b-modal.modal-endorse>Endorse</b-button>
      <b-button v-else variant="success" disabled>You've endorsed this policy!</b-button>
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
          <b-button variant="danger" @click="handleCancel">
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
    politician: Object
  },
  data() {
    return {
      stanceText: '',
      isSubmitting: false,
    };
  },
  methods: {
    async handleSubmit() {
      const stanceData = {
        policy_id: this.policy.id,
        politician_id: this.politician.id,
        content: this.stanceText,
      };

      try {
        this.isSubmitting = true;
        await ApiUtil.postStance(stanceData);
        const stanceResponse = await ApiUtil.getStance(this.politician.id);
        const allPoliticianStances = stanceResponse.data;
        const mostRecentStancePolicyId = allPoliticianStances[allPoliticianStances.length - 1].policy_id;
        this.politician.hasEndorsed = (mostRecentStancePolicyId === this.policy.id);
      } catch (error) {
        alert('Oops, something went wrong.');
      }
      this.isSubmitting = false;
      this.stanceText = '';
      this.$refs['modal-endorse'].hide();
    },
    handleCancel() {
      this.stanceText = '';
      this.$refs['modal-endorse'].hide();
    },
    focusTextarea() {
      this.$refs.focusText.focus();
    },
  },
};
</script>

<style lang="scss" scoped></style>
