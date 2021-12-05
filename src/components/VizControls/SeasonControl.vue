<template>
  <v-row class="pa-2 pb-1">
    <v-col cols="1" class="mr-5">
      <v-row class="d-inline-flex">
        <v-select
          :items="options"
          v-model="selected"
          label="Season"
          dense
          hide-details
          @change="change"
        ></v-select>
      </v-row>
    </v-col>
  </v-row>
</template>

<script>
import { Hub } from 'aws-amplify';
import { DEFAULT_SEASON, DEFAULT_SEASON_OPTIONS } from '@/globals/compare';
import { KEY_SEASON} from '@/globals/keys';

export default {
  name: 'SeasonControl',
  data() {
    return {
      options: DEFAULT_SEASON_OPTIONS,
      selected: localStorage.getItem(KEY_SEASON) || DEFAULT_SEASON
    }
  },
  methods: {
    change() {
      Hub.dispatch('SeasonFilter', {
        data : this.selected
      });
    }
  }
}
</script>