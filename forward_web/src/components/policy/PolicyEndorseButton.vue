<template>
  <div>
    <div v-if="isPolitician && isLoading">
      <b-spinner type="grow" label="Loading..."></b-spinner>
    </div>
    <div v-else>
      <b-button v-if="isPolitician && !hasEndorsed" variant="primary" v-b-modal.modal-endorse>Endorse</b-button>
      <b-button v-else-if="isPolitician && hasEndorsed" variant="success" disabled>You've endorsed this policy!</b-button>
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
  },
  data() {
    return {
      stanceText: '',
      isPolitician: false,
      politicianId: 0,
      isLoading: true,
      isSubmitting: false,
      hasEndorsed: false,
    };
  },
  async created() {
    const currentUser = this.$store.getters.getUserInfo;
    if (currentUser.approved) {
      this.isPolitician = true;
      this.politicianId = currentUser.politician_id;
      try {
        const stanceResponse = await ApiUtil.getStance(this.politicianId);
        const allPoliticianStances = stanceResponse.data;
        allPoliticianStances.forEach(stanceObject => {
          if (stanceObject.policy_id === this.policy.id) {
            this.hasEndorsed = true;
          }
        });
      } catch (error) {
        alert('Opps, something went wrong in checking your endorsments!');
      }
    }
    this.isLoading = false;
  },
  methods: {
    async handleSubmit() {
      const stanceData = {
        policy_id: this.policy.id,
        politician_id: this.politicianId,
        content: this.stanceText,
      };

      try {
        this.isSubmitting = true;
        await ApiUtil.postStance(stanceData);
        const stanceResponse = await ApiUtil.getStance(this.politicianId);
        const allPoliticianStances = stanceResponse.data;
        const mostRecentStancePolicyId = allPoliticianStances[allPoliticianStances.length - 1].policy_id;
        this.hasEndorsed = (mostRecentStancePolicyId === this.policy.id);
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
