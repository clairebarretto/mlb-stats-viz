<template>
  <v-alert
    text
    dense
    light
    color="grey darken-1"
    class="text-center mt-7 mb-7"
    v-text="title">
  </v-alert>
</template>

<script>
export default {
  name: 'TitleBar',
  props: ['title']
};
</script>