<template>
  <div class="democrat-list">
    <button type="button" id="get-politicians" @click="fetchInit">
      Politicians
    </button>
    <div v-if="avail == true">
      <i>{{ res }}</i>
    </div>
    <p>Hi</p>
  </div>
</template>

<script>
export default {
  name: "DemocratList",
  data() {
    return {
      avail: false,
      res: false,
    };
  },
  methods: {},
};
</script>
