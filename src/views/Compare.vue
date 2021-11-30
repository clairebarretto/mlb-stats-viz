<template>
  <div>
    <v-alert
      border="bottom"
      class="mb-8"
      colored-border
      color="grey lighten-2"
    >
      Hello!
    </v-alert>
    <v-row>
      <v-col v-for="id in playerIds" :key="id" :cols="3" class="pt-0">
        <Card :id="id" />
      </v-col>
    </v-row>
  </div>
</template>

<script>
import Card from '@/components/CompareCard/Card'

export default {
  name: 'App',

  components: {
    Card
  },

  data: () => ({
    playerIds: [
      641487,
      // 664034,
      // 571745,
      // 572122,
    ]
  }),
};
</script>

<style>
  .v-card__title,
  .v-card__text {
      font-weight: 300;
  }
</style>