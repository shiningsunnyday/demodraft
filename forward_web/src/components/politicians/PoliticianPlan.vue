<template>
  <LoadingSpinner v-if="isLoading"></LoadingSpinner>
  <b-container v-else class="plan">
    <h1>{{ policy.name }}</h1>
    <p>{{ politician.first }} {{ politician.last }}'s Plan</p>
    <div v-if="hasPlan">
      <!-- plan table -->
      <b-table 
        :items="items" 
        :fields="fields" 
        striped 
        hover
      ></b-table>
    </div>

    <!-- Add plan -->
    <div v-else>
      <p>*Must have atleast two steps to post a plan*</p>
      <div v-if="hasAddedStep">
        <div v-if="isCurrentPolitician" class="plan__button-container">
          <b-button @click="showAddStepModal">
            Add Step
          </b-button>
          <b-button v-if="isSaving" disabled>
            Saving...
          </b-button>
          <b-button v-else-if="items.length < 2" disabled>
            Save
          </b-button>
          <b-button v-else @click="savePlan">
            Save
          </b-button>
        </div>

        <!-- plan table -->
        <b-table :items="items" :fields="fields" striped hover>
          <!-- <template v-slot:cell(actions)="row">
          <b-button>
            Edit
          </b-button>
        </template> -->
        </b-table>
      </div>

      <!-- no plan -->
      <div v-else class="plan__no-plan-container">
        <div v-if="isCurrentPolitician">
          <b-button @click="showAddStepModal">
            Add Step
          </b-button>
        </div>
      </div>

      <!-- modal -->
      <b-modal
        :title="`Add Step ${currentStep}`"
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
          <p class="plan__small-text">{{ charactersLeft }}/120</p>
        </b-form>

        <!-- modal footer -->
        <template v-slot:modal-footer>
          <b-button v-if="planText.length < 1" disabled>Submit</b-button>
          <b-button v-else variant="primary" @click="handleSubmit">
            Submit
          </b-button>
          <b-button variant="danger" @click="hideAddStepModal">
            Cancel
          </b-button>
        </template>
      </b-modal>
    </div>
  </b-container>
</template>

<script>
import { PolicyService, PoliticianService } from '@/services';

export default {
  name: 'PoliticianPlan',
  props: {
    pushedPolitician: Object,
    pushedPolicy: Object,
  },
  data() {
    return {
      // fields: ['step', 'plan', 'actions'],
      fields: ['step', 'plan'],
      items: [],
      steps: [],
      modalId: 'modal-plan',
      planText: '',
      policy: {},
      politician: {},
      isLoading: true,
      hasPlan: false,
      isSaving: false,
    };
  },
  async created() {
    const { politicianId, policyId } = this.$route.params;

    if (this.pushedPolitician && this.pushedPolicy) {
      this.politician = this.pushedPolitician;
      this.policy = this.pushedPolicy;
    } else {
      try {
        this.policy = await PolicyService.getPolicy(policyId);
        this.politician = await PoliticianService.getPolitician(politicianId);
      } catch (error) {
        alert('error on politician plan');
      }
    }
    
    try {
      const response = await PoliticianService.getPlan({
        policy_id: policyId,
        politician_id: politicianId
      });

      const { steps } = response.data;
      for (const step of steps) {
        this.items.push({
          step: this.items.length + 1,
          plan: step,
        });
      }
      this.hasPlan = true;
    } catch (error) {
      if (error.response.status !== 400) {
        alert(error);
        return;
      }
    }
    
    this.isLoading = false;
  },
  computed: {
    isCurrentPolitician() {
      const user = this.$store.getters.userState;
      return user.politician_id === this.politician.id;
    },
    hasAddedStep() {
      return this.items.length >= 1;
    },
    charactersLeft() {
      return this.planText.length;
    },
    currentStep() {
      return this.items.length + 1;
    },
  },
  methods: {
    handleSubmit() {
      this.addNewStep();
      this.hideAddStepModal();
    },
    addNewStep() {
      const newStep = {
        step: this.items.length + 1,
        plan: this.planText,
      };
      this.items.push(newStep);
      this.steps.push(this.planText);
    },
    async savePlan() {
      this.isSaving = true;
      const user = this.$store.getters.userState;
      const data = {
        steps: this.steps,
        politician_id: this.politician.id,
        policy_id: this.policy.id,
        scope: 'local',
      };

      try {
        await PoliticianService.postPlan(data, user);
        await this.$store.dispatch('setPolitician', user);
      } catch (error) {
        alert(error);
      }
      location.reload();
    },
    showAddStepModal() {
      this.$bvModal.show(this.modalId);
    },
    hideAddStepModal() {
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
  &__button-container {
    > * {
      margin-right: 8px;
      margin-bottom: 8px;
    }
  }

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
