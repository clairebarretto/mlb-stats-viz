<template>
  <v-sheet
    class="text-center"
    color="#fbfbfb"
    height="150"
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
  props: ['meta']
}
</script>

<style>
  .loading {
    height: 100px;
  }
</style>