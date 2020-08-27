<template>
  <div class="comments-wrapper__lead-comment">
    <p class="comments-wrapper__username"></p>
    <p class="comments-wrapper__content"></p>
    <div class="comments-wrapper__options">
      <div class="comments-wrapper__like">
        <span></span>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  name: 'CommentCard',
};
</script>

<style lang="scss" scoped>
.comments-wrapper {
  &__lead-comment {
    padding: 10px;
    border: 1px solid rgb(224, 224, 224);
    margin-bottom: 8px;
    height: 150px;
  }

  &__username {
    height: 40px;
    background: grey;
  }

  &__options {
    display: flex;
  }

  &__like {
    display: flex;
    align-items: center;
  }
}
</style>
