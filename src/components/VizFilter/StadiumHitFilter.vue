<template>
  <v-row class="d-inline-flex">
    <v-checkbox
      class="mr-5"
      color="green"
      dense
      hide-details
      label="1B"
      v-model="selected"
      value="single"
      @change="change"
    ></v-checkbox>
    <v-checkbox
      class="mr-5"
      color="red"
      dense
      hide-details
      label="2B"
      v-model="selected"
      value="double"
      @change="change"
    ></v-checkbox>
    <v-checkbox
      class="mr-5"
      color="orange"
      dense
      hide-details
      label="3B"
      v-model="selected"
      value="triple"
      @change="change"
    ></v-checkbox>
    <v-checkbox
      class="mr-0"
      color="purple"
      dense
      hide-details
      label="HR"
      v-model="selected"
      value="home_run"
      @change="change"
    ></v-checkbox>
  </v-row>
</template>

<script>
import { Hub } from 'aws-amplify';

export default {
  name: 'StadiumHitFilter',
  props: ['filters'],
  data() {
    return {
      selected: this.filters
    }
  },
  methods: {
    change() {
      Hub.dispatch('StadiumHitFilter', {
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