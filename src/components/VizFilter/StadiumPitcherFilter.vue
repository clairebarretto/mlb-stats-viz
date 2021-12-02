<template>
  <v-select
    :items="options"
    v-model="selected"
    label="LHP / RHP"
    dense
    hide-details
    @change="change"
  ></v-select>
</template>

<script>
import { Hub } from 'aws-amplify';

export default {
  name: 'StadiumPitcherFilter',
  props: ['pitcher_type'],
  data() {
    return {
      selected: this.pitcher_type,
      options: [
        {text: 'Both', value: 'both'},
        {text: 'vs. LHP', value: 'L'},
        {text: 'vs. RHP', value: 'R'}
      ],
    }
  },
  methods: {
    change() {
      Hub.dispatch('StadiumPitcherFilter', {
        data : this.selected
      });
    }
  },
  watch: {
    pitcher_type() {
      this.selected = this.pitcher_type;
    }
  }
}
</script>