<template>
  <DynamicScroller
    :items="filteredPolicies"
    :min-item-size="54"
    class="scroller"
  >
    <template v-slot="{ policy, index, active }">
      <DynamicScrollerItem
        :item="policy"
        :active="active"
        :size-dependencies="[policy.name]"
        :data-index="index"
      >
        <div class="name">{{policy.name}}</div>
        <!-- <BCard class="mb-2 policy__card">
          <b-card-title>
            <b-button
              variant="link"
              v-b-toggle
              :href="`#collapse-${policy.id}`"
              @click.prevent
            >
              {{ policy.name }}
            </b-button>
          </b-card-title>
          <b-collapse :id="`collapse-${policy.id}`" class="mt-2">
            <BCard>
              <p class="card-text">{{ policy.statement }}</p>
              <BButton variant="link">
                <router-link
                  class="policy__route"
                  v-bind:to="{
                    name: 'policy-page',
                    params: {
                      id: policy.id,
                    },
                  }"
                >
                  Learn more
                </router-link>
              </BButton>
            </BCard>
          </b-collapse>
          <b-card-text class="policy__category">
            Category: {{ policy.category }}
          </b-card-text>
        </BCard> -->
      </DynamicScrollerItem>
    </template>
  </DynamicScroller>
  <!-- <div
      class="policy__card-wrapper"
      v-for="policy in filteredPolicies"
      :key="policy.id"
    >
      <BCard class="mb-2 policy__card">
        <b-card-title>
          <b-button
            variant="link"
            v-b-toggle
            :href="`#collapse-${policy.id}`"
            @click.prevent
          >
            {{ policy.name }}
          </b-button>
        </b-card-title>
        <b-collapse :id="`collapse-${policy.id}`" class="mt-2">
          <BCard>
            <p class="card-text">{{ policy.statement }}</p>
            <BButton variant="link">
              <router-link
                class="policy__route"
                v-bind:to="{
                  name: 'policy-page',
                  params: {
                    id: policy.id,
                  },
                }"
              >
                Learn more
              </router-link>
            </BButton>
          </BCard>
        </b-collapse>
        <b-card-text class="policy__category">
          Category: {{ policy.category }}
        </b-card-text>
      </BCard>
    </div> -->
</template>

<script>
import { BCard, BButton } from 'bootstrap-vue';

export default {
  name: 'PolicyList',
  components: {
    'b-button': BButton,
    'b-card': BCard,
  },
  props: {
    filteredPolicies: {
      type: Array,
      required: true,
    },
  },
};
</script>

<style lang="scss" scoped>
.scroller {
  height: 100%;
}

.name {
  height: 54%;
  padding: 0 12px;
  display: flex;
  align-items: center;
}
// .policy {
//   display: flex;
//   flex-wrap: wrap;
//   justify-content: center;

//   &__card-wrapper {
//     margin: 20px;
//   }

//   &__card {
//     width: 300px;
//     @media screen and (min-width: 768px) {
//       width: 455px;
//     }
//     //cursor: pointer;
//   }

//   &__route {
//     text-decoration: none;
//     color: unset;
//   }

//   &__category {
//     margin-top: 1em;
//   }
// }
</style>
