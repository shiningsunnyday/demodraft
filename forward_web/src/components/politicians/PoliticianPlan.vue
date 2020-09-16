<template>
  <b-container class="plan">
    <!-- plan -->
    <div v-if="hasPlan">
      <h1>
        Politician Plan
        <b-button v-if="isPolitician" @click="showAddPlanModal">
          Add Plan
        </b-button>
      </h1>

      <!-- plan table -->
      <b-table :items="items" :fields="fields" striped hover>
        <template v-slot:cell(actions)="row">
          <b-button>
            Edit
          </b-button>
        </template>
      </b-table>
      <!-- /// -->
    </div>
    <!-- /// -->

    <!-- no plan -->
    <div v-else class="plan__no-plan-container">
      <h1>
        Politician Plan
        <b-button v-if="isPolitician" @click="showAddPlanModal">
          Add Plan
        </b-button>
      </h1>
      <p>This politician has no plan yet, booo!</p>
    </div>
    <!-- /// -->

    <!-- modal -->
    <b-modal
      title="Add Your Plan"
      :id="modalId"
      @shown="focusTextArea"
      centered
      no-close-on-backdrop
    >
      <!-- modal form -->
      <b-form>
        <b-form-textarea
          v-model="planText"
          ref="focusText"
          no-auto-shrink
          maxlength="120"
        />
        <p class="plan__small-text">
          {{ charactersLeft }}/120
        </p>
      </b-form>
      <!-- /// -->

      <!-- modal footer -->
      <template v-slot:modal-footer>
        <b-button v-if="planText.length < 1" disabled>Submit</b-button>
        <b-button v-else variant="primary" @click="handleSubmit">
          Submit
        </b-button>
        <b-button variant="danger" @click="hideAddPlanModal">
          Cancel
        </b-button>
      </template>
      <!-- /// -->
    </b-modal>
    <!-- /// -->
  </b-container>
</template>

<script>
export default {
  name: 'PoliticianPlan',
  props: {
    id: String,
    politician: Object,
    isPushed: Boolean,
  },
  data() {
    return {
      fields: ['step', 'plan', 'actions'],
      items: [],
      modalId: 'modal-plan',
      planText: '',
    };
  },
  created() {
    // TODO - fetch politician plan from id
    // fill this.items with response
  },
  computed: {
    isPolitician() {
      const user = this.$store.getters.userState;
      return user.approved;
    },
    hasPlan() {
      return this.items.length >= 1;
    },
    charactersLeft() {
      return this.planText.length;
    }
  },
  methods: {
    handleSubmit() {
      this.addNewPlan();
      this.hideAddPlanModal();
    },
    addNewPlan() {
      const newPlan = {
        step: this.items.length + 1,
        plan: this.planText,
      };
      this.items.push(newPlan);
    },
    showAddPlanModal() {
      this.$bvModal.show(this.modalId);
    },
    hideAddPlanModal() {
      this.$bvModal.hide(this.modalId);
      this.planText = '';
    },
    focusTextArea() {
      this.$refs.focusText.focus();
    },
  },
};
</script>

<style lang="scss" scoped>
.plan {
  &__no-plan-container {
    display: inline-flex;
    flex-direction: column;
  }

  &__small-text {
    font-size: 12px;
    padding: 0;
    margin: 8px 0 0 0;
    text-align: right;
  }
}
</style>
