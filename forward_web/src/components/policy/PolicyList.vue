<template>
  <div class="policy-list-container">
    <div v-if="isFiltering">
      <div class="policy-list__policies">
        <PolicyCard 
          v-for="policy in filteredPolicies" 
          :key="policy.id" 
          :policy="policy"
        >
        </PolicyCard>
      </div>
    </div>
    <div v-else class="policy-list__categories">
      <div 
        v-for="category of groupedCategories" 
        :key="category.id"
        class="policy-list__policies-container"
      >
        <div class="policy-list__header">
          <h3 class="policy-list__title">
            {{ category.name.charAt(0).toUpperCase() + category.name.slice(1) }}
          </h3>
          <b-button 
            @click="handleSeeMore(category.name)"
            variant="link" 
            class="policy-list__see-more"
          >
            see more >>
          </b-button>
        </div>
        
        <div class="policy-list__policies">
          <PolicyCard 
            v-for="n in 3" 
            :key="category.policies[n].id" 
            :policy="category.policies[n]"
          >
          </PolicyCard>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { BCard, BButton } from 'bootstrap-vue';
import PolicyCard from './PolicyCard';
import { ApiUtil } from '@/_utils/api-utils';
import * as Config from '@/config.json';

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
    filterPolicies: Function,
    selectedValues: Array,
    isFiltering: Boolean
  },
  data() {
    return {
    };
  },
  computed: {
    /**
     * returns an object
     * { 
     *  id: { name: policy.categoryName, policies: [...policy] }
     * }
     */
    groupedCategories() {
      const groups = {};
      this.filteredPolicies.forEach((policy) => {
        const id = policy.category;
        if (!groups[id]) {
          groups[id] = {
            name: policy.categoryName,
            policies: [policy],
          };
        } else {
          groups[id].policies.push(policy);
        }
      });
      return groups;
    }
  },
  methods: {
    handleSeeMore(category) {
      this.selectedValues.push(category);
      this.filterPolicies();
      window.scrollTo(0,0);
    }
  }
};
</script>

<style lang="scss" scoped>
.policy-list-container {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
}

.policy-list {

  &__header {
    display: flex;
    justify-content: center;
    > * {
      margin: 0 4px;
    }
  }

  &__title {
    font-weight: bold;
  }
  
  &__categories{
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
  }

  &__policies-container{
    margin: 1.5rem 0;
  }

  &__policies {
    display: flex;
    align-items: center;
    justify-content: center;
    flex-wrap: wrap;
  }
}
</style>
