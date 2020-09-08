<template>
  <div class="policy-list">
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
          <h3>
            {{ category.name.charAt(0).toUpperCase() + category.name.slice(1)}}
          </h3>
          <b-button 
            v-if="category.policies.length > 3"
            @click="handleSeeMore(category.name)"
            class="policy-list__see-more"
            variant="link"
          >see more >></b-button>
        </div>

        <div v-if="category.policies.length >= 3" class="policy-list__policies">
          <PolicyCard
            v-for="(n, index) in 3"
            :key="category.policies[index].id"
            :policy="category.policies[index]"
          >
          </PolicyCard>
        </div>

        <div v-else class="policy-list__policies">
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
    filterPolicies: Function,
    selectedValues: Array,
    isFiltering: Boolean,
  },
  data() {
    return {};
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
    },
  },
  methods: {
    handleSeeMore(category) {
      this.selectedValues.push(category);
      this.filterPolicies();
      window.scrollTo(0, 0);
    },
  },
};
</script>

<style lang="scss" scoped>
@import '@/_styles';

@mixin tablet-media-query {
  @media screen and (min-width: $tablet-breakpoint) {
    @content;
  }
}

.policy-list {
  &__header {
    display: flex;
    flex-direction: column;

    @include tablet-media-query {
      flex-direction: row;
      align-items: center;
      padding-left: 10px;
    }

    h3 {
      padding: 0;
      margin: 0;
    }
  }

  &__see-more {
    font-weight: bold;
  }

  &__categories {
    display: flex;
    flex-direction: column;
    flex-wrap: wrap;
    justify-content: center;
  }

  &__policies-container {
    margin: 1.5rem auto;
  }

  &__policies {
    display: flex;
    align-items: center;
    justify-content: flex-start;
    flex-wrap: wrap;

    @include tablet-media-query {
      justify-content: center;
    }
  }
}
</style>
