<template>
  <div class="selected-politician">
    <h1>{{ politician.first }} {{ politician.last }}</h1>
    <div class="selected-politician__img-wrapper">
      <img
        src="https://i.picsum.photos/id/1025/4951/3301.jpg?hmac=_aGh5AtoOChip_iaMo8ZvvytfEojcgqbCH7dzaz-H8Y"
      />
    </div>

    <div class="selected-politician__description">
      <p>Running for {{ politician.name }}</p>
      <p v-if="politician.actblue">
        Actblue: <a :href="politician.actblue" target="_blank" rel="noopener noreferrer">{{ politician.actblue }}</a>
      </p>
    </div>

    <div class="selected-politician__policies">
      <div class="selected-politician__wrapper">
        <div class="selected-politician__policy-list">
          <h3>Endorsed:</h3>
          <ul v-for="policy in endorsed" v-bind:key="policy.id">
            <router-link
              class="selected-politician__route"
              v-bind:to="{
                name: 'policy-page',
                params: {
                  id: policy.id,
                },
              }"
            >
              {{ policy.name }}
            </router-link>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ApiUtil } from '@/_utils/api-utils';

export default {
  name: "SelectedPolitician",
  data() {
    return {
      politician: {},
      endorsed: [],
      stances: [],
    };
  },
  async created() {
    this.politician = await ApiUtil.getSelectedPolitician(
      this.$route.params.id
    );

    const stanceResponse = await ApiUtil.getStance(this.politician.id);
    this.stances = stanceResponse.data;
    
    const policySet = new Set();
    this.stances.forEach(stance => {
      if (!policySet.has(stance.policy_id)) {
        policySet.add(stance.policy_id);
        this.endorsed.push({'name': stance.policy_name, 'id': stance.policy_id});
      }
    });
    // todo
    // show most recent stance when user clicks an endorsed policy
    console.log('endorsed: ', this.endorsed);
    console.log('politician: ', this.politician);
  },
};
</script>

<style lang="scss" scoped>
.selected-politician {
  display: flex;
  flex-direction: column;
  align-items: center;

  &__img-wrapper {
    max-width: 700px;
    max-height: 700px;

    img {
      width: 100%;
    }
  }

  &__description {
    margin-top: 20px;
  }

  &__policies {
    display: flex;
    flex-direction: row;
    justify-content: center;
    margin-top: 20px;
    width: 100%;
  }

  &__wrapper {
    display: flex;
    flex-direction: row;
    justify-content: center;
    flex-wrap: wrap;
    width: 500px;
    padding: 0 20px;
  }

  &__policy-list {
    // max-width: 300px;
    text-align: center;
  }
}
</style>
