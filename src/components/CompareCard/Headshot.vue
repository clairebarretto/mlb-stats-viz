<template>
  <v-img v-if="this.meta" :src="this.meta.HeadshotPhotoUrl" class="headshot"></v-img>
</template>

<script>
export default {
  name: 'Actionshot',
  props: ['meta']
}
</script>

<style>
  .headshot {
    width: 80px;
    height: 110px;
    border: 2px solid white;
    top: -20px;
    right: 20px;
    float: right;
  }
</style>