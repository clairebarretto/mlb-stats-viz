<template>
  <v-img v-if="url" :src="url" class="headshot"></v-img>
</template>

<script>
export default {
  name: 'Actionshot',
  props: ['url']
}
</script>

<style>
  .headshot {
    width: 80px;
    height: 110px;
    border: 2px solid #fff;
    top: -20px;
    right: 20px;
    float: right;
  }
</style>