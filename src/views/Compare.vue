<template>
  <div>
    <v-alert
      border="bottom"
      class="mb-8"
      colored-border
      color="grey lighten-2"
    >
      <SeasonControl />
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
import SeasonControl from '@/components/VizControls/SeasonControl'
import {
    DEFAULT_PLAYER1,
    DEFAULT_PLAYER2,
    DEFAULT_PLAYER3,
    DEFAULT_PLAYER4,
    KEY_PLAYER1,
    KEY_PLAYER2,
    KEY_PLAYER3,
    KEY_PLAYER4,
} from '@/globals/compare';

export default {
  name: 'App',
  components: {
    Card,
    SeasonControl
  },
  data: () => ({
    playerIds: [
      localStorage.getItem(KEY_PLAYER1) || DEFAULT_PLAYER1,
      localStorage.getItem(KEY_PLAYER2) || DEFAULT_PLAYER2,
      localStorage.getItem(KEY_PLAYER3) || DEFAULT_PLAYER3,
      localStorage.getItem(KEY_PLAYER4) || DEFAULT_PLAYER4
    ]
  })
};
</script>

<style>
  .v-card__title,
  .v-card__text {
      font-weight: 300;
  }
</style>