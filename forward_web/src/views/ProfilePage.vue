<template>
  <div class="profile">
    <h1 class="profile__title">Profile</h1>
    <b-container class="profile__container">
      
      <div class="profile__user-container">
        <h2 class="profile__header">{{ username }}</h2>
        <p>123 score</p>
      </div>

      <h3 class="profile__header --normalize">Badges</h3>
      <div class="profile__badges-container">
        <div v-if="isMod" class="profile__badge-wrapper">
          <img src="../_assets/moderator.png" alt="">
          <p>Moderator</p>
        </div>
        <!-- <div v-if="isMod" class="profile__badge-wrapper">
          <img src="../_assets/moderator.png" alt="">
          <p>Moderator</p>
        </div>
        <div v-if="isMod" class="profile__badge-wrapper">
          <img src="../_assets/moderator.png" alt="">
          <p>Moderator</p>
        </div>
        <div v-if="isMod" class="profile__badge-wrapper">
          <img src="../_assets/moderator.png" alt="">
          <p>Moderator</p>
        </div>
        <div v-if="isMod" class="profile__badge-wrapper">
          <img src="../_assets/moderator.png" alt="">
          <p>Moderator</p>
        </div> -->
      </div>
    </b-container>
  </div>
</template>

<script>
export default {
  name: 'profile-page',
  data() {
    return {
      username: '',
      score: 0,
      isMod: false,
    };
  },
  created() {
    const user = this.$store.getters.getUserInfo;
    this.username = user.username;
    this.isMod = user.isMod;
  }
};
</script>

<style lang="scss" scoped>
.profile {
  height: 100vh;
  padding: 0 1em;

  &__header {
    font-weight: bold;
  }

  &__title {
    text-align: center;
    margin-bottom: 5rem;
  }
  &__container {
    display: flex;
    flex-direction: column;
    align-items: center;
    background: rgb(238, 238, 238);
  }

  &__user-container{
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 1em;
  }

  &__badges-container {
    display: flex;
    flex-wrap: wrap;
  }

  &__badge-wrapper {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 1em;
  }

  p {
    padding: 0;
    margin: 0;
  }
}
.--normalize {
  font-size: 1rem;
  padding: 0;
  margin: 0;
}
</style>
