<template>
  <v-sheet
    class="text-center"
    color="#fbfbfb"
    :height="height"
  >
    <v-progress-linear
        indeterminate
        color="grey"
        class="mb-7"
    ></v-progress-linear>
    <span class="body-1 grey--text">Loading...</span>
  </v-sheet>
</template>

<script>
export default {
  name: 'Actionshot',
  props: ['fill'],
  data() {
    return {
      height: this.fill ? '100vh' : '150'
    }
  }
}
</script>

<style>
  .loading {
    height: 100px;
  }
</style>