<template>
  <v-row class="pa-2 pb-1">
    <v-col cols="1" class="mr-5">
      <v-row class="d-inline-flex">
        <v-select
          :items="seasons"
          v-model="season"
          label="Season"
          dense
          hide-details
        ></v-select>
      </v-row>
    </v-col>
    <v-col cols="1" class="mr-5">
      <v-row class="d-inline-flex">
        <v-select
          :items="player_counts"
          v-model="player_count"
          label="Player Count"
          dense
          hide-details
        ></v-select>
      </v-row>
    </v-col>
  </v-row>
</template>

<script>
import { Hub } from 'aws-amplify';

export default {
  props: ['filters'],
  data() {
    return {
      seasons: ['2021'],
      season: '2021',
      player_counts: ['4'],
      player_count: '4'
    }
  },
  methods: {
    change() {
      Hub.dispatch('Filter', {
        data : this.selected
      });
    }
  },
  watch: {
    filters() {
      this.selected = this.filters;
    }
  }
}
</script>