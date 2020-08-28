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
        <h3 class="policy-list__title">{{ category.name }}</h3>
        <div class="policy-list__policies">
          <PolicyCard 
            v-for="policy in category.policies" 
            :key="policy.id" 
            :policy="policy"
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
    isFiltering: Boolean
  },
  data() {
    return {
    };
  },
  computed: {
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
};
</script>

<style lang="scss" scoped>
.policy-list-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
}

.policy-list {
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
