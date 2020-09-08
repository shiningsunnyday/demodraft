<template>
  <div class="profile">
    <h1 class="profile__title">Profile</h1>
    <b-container class="profile__container">
      <div class="profile__user-section">
        <h2 class="profile__header">{{ username }}</h2>
        <!-- <p><span class="--highlight">{{ score }}</span> score</p> -->
      </div>
      
      <div class="profile__badge-section">
        <h3 class="profile__header --normalize">Badges</h3>
        <!-- TODO - vuex to scale accordingly with more badges -->  
        <div v-if="isPolitician || isMod" class="profile__badges-container">
          <div v-if="isMod" class="profile__badge-wrapper">
            <img src="../_assets/moderator.png" alt="" />
            <p>Moderator</p>
          </div>
          <div v-if="isPolitician" class="profile__badge-wrapper">
            <img src="../_assets/politician.png" alt="" />
            <p>Politician</p>
          </div>
        </div>
        <p v-else>Feels a bit empty in here...</p>
      </div>
    </b-container>
  </div>
</template>

<script>
import { ApiUtil } from '@/_utils/api-utils';

export default {
  name: 'profile-page',
  data() {
    return {
      score: 0,
      user: this.$store.getters.userState,
    };
  },
  // async created() {
  //   // TODO - store score in vuex state during login
  //   try {
  //     this.score = await ApiUtil.getUserScore({ 
  //       user_id: this.user.id, 
  //       username: this.user.username,
  //       password: this.user.password
  //     });
  //   } catch (error) {
  //     console.error(error);
  //   }
  // },
  computed: {
    isPolitician() {
      return this.user.approved;
    },
    isMod() {
      return this.user.isMod;
    },
    username() {
      return this.user.username;
    },
  },
};
</script>

<style lang="scss" scoped>
@mixin flex-column-center {
  display: flex;
  flex-direction: column;
  align-items: center;
}

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
    @include flex-column-center;
    justify-content: center;
    background: rgb(243, 243, 243);
    height: 300px;
  }

  &__user-section {
    @include flex-column-center;
    padding: 1em;
  }

  &__badge-section {
    @include flex-column-center;
  }

  &__badges-container {
    display: flex;
    flex-wrap: wrap;
  }

  &__badge-wrapper {
    @include flex-column-center;
    padding: 1em;
  }

  p {
    padding: 0;
    margin: 0;
  }

  .--normalize {
    font-size: 1rem;
    padding: 0;
    margin: 0;
  }

  .--highlight {
    color: #1C94DC;
  }
}
</style>
