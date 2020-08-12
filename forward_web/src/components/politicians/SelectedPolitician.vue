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
          <h3>Supports:</h3>
          <p>Policy A</p>
          <p>Policy B</p>
          <p>Policy C</p>
        </div>

        <div class="selected-politician__policy-list">
          <h3>Rejects:</h3>
          <p>Policy 1</p>
          <p>Policy 2</p>
          <p>Policy 3</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ApiUtil } from "../../_utils/api-utils";

export default {
  name: "SelectedPolitician",
  data() {
    return {
      politician: {},
    };
  },
  async created() {
    this.politician = await ApiUtil.getSelectedPolitician(
      this.$route.params.id
    );

    console.log(this.politician);
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
    justify-content: space-between;
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
