<template>
  <div>
    <v-img v-if="!url" src="@/assets/images/baseball-header.jpg" style="height: 140px; opacity: 0.3"></v-img>
    <v-img v-else :src="url" style="height: 140px;"></v-img>
  </div>
</template>

<script>
export default {
  name: 'Actionshot',
  props: ['url']
}
</script>