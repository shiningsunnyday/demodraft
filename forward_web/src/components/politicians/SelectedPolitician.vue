<template>
  <div class="selected-politician">
    <h1>{{politician.name}}</h1>
    <div class="selected-politician__img-wrapper">
      <img src="https://i.picsum.photos/id/1025/4951/3301.jpg?hmac=_aGh5AtoOChip_iaMo8ZvvytfEojcgqbCH7dzaz-H8Y" />
    </div>
    
    <div class="selected-politician__policies">
      <div class="policies__policy-list">
        <h3>Supports:</h3>
        <ul>
          <li>Policy A</li>
          <li>Policy B</li>
          <li>Policy C</li>
        </ul>
      </div>

      <div class="policies__policy-list">
        <h3>Rejects:</h3>
        <ul>
          <li>Policy 1</li>
          <li>Policy 2</li>
          <li>Policy 3</li>
        </ul>
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
    await console.log(this.politician);
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

  &__policies {
    display: flex;
    flex-direction: row;
    justify-content: space-evenly;
    margin-top: 20px;
    
    &__policy-list{
      h3 {
        color: red;
      }
    }
  }
}
</style>
