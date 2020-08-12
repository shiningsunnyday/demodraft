<template>
  <div class="policy">
    <div
      class="policy__card-wrapper"
      v-for="policy in filteredPolicies"
      :key="policy.id"
    >
      <PolicyCard
        :policy="policy"
        @handle-policy-name="handlePolicyName"
      ></PolicyCard>
    </div>
    <b-modal 
      ref="modal-endorse" 
      id="modal-endorse" 
      :title="modalTitle"
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
        <br />
        <p>Preview</p>
        <hr />
        <pre class="mt-3 mb-0">{{ stanceText }}</pre>
      </b-form>
      <template v-slot:modal-footer>
        <b-button v-if="stanceText.length < 1" disabled>Submit</b-button>
        <b-button v-else variant="primary" @click="handleSubmit">
          Submit
        </b-button>
        <b-button variant="danger" @click="handleCloseModal">
          Cancel
        </b-button>
      </template>
    </b-modal>
  </div>
</template>

<script>
import { BCard, BButton } from 'bootstrap-vue';
import PolicyCard from './PolicyCard';

export default {
  name: 'PolicyList',
  components: {
    'b-button': BButton,
    'b-card': BCard,
    PolicyCard,
  },
  props: {
    filteredPolicies: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      modalTitle: '',
      stanceText: '',
    };
  },
  methods: {
    handlePolicyName(event) {
      this.modalTitle = event;
    },
    handleSubmit() {
      console.log(this.stanceText);
      this.stanceText = '';
    },
    handleCloseModal() {
      this.stanceText = '';
      this.$refs['modal-endorse'].hide();
    },
    focusTextarea() {
      this.$refs.focusText.focus();
    }
  },
};
</script>

<style lang="scss" scoped>
.policy {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;

  &__card-wrapper {
    margin: 20px;
  }

  &__card {
    width: 300px;
    @media screen and (min-width: 768px) {
      width: 455px;
    }
    //cursor: pointer;
  }

  &__route {
    text-decoration: none;
    color: unset;
  }

  &__category {
    margin-top: 1em;
  }
}
</style>
