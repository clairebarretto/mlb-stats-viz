<template>
  <v-img v-if="this.meta" :src="this.meta.ActionPhotoUrl" style="height: 140px;"></v-img>
</template>

<script>
export default {
  name: 'Actionshot',
  props: ['meta']
}
</script>