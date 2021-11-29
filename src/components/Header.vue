<template>
  <div>
    <v-app-bar
      color="grey darken-4"
      dark
      hide-on-scroll
      dense>
      <v-icon>mdi-baseball</v-icon>
      <v-tabs align-with-title>
          <v-tab>Compare Hitters</v-tab>
      </v-tabs>
  </v-app-bar>
  </div>
</template>

<script>
export default {
  name: "Header"
};
</script>