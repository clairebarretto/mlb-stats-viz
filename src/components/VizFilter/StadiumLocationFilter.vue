<template>
  <v-select
    :items="options"
    v-model="selected"
    label="Home / Away"
    dense
    hide-details
    @change="change"
  ></v-select>
</template>

<script>
import { Hub } from 'aws-amplify';

export default {
  name: 'StadiumLocationFilter',
  props: ['location_type'],
  data() {
    return {
      selected: this.location_type,
      options: [
        {text: 'Both', value: 'both'},
        {text: 'Home', value: 'home'},
        {text: 'Away', value: 'away'}
      ]
    }
  },
  methods: {
    change() {
      Hub.dispatch('StadiumLocationFilter', {
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