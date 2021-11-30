<template>
  <Loading v-if="!statcast.length" />
  <div v-else class="mt-15 mb-15">
    <v-row>
      <v-col cols="6">
        <v-row justify="center">
          <div
            class="pa-1 stat"
            @mouseover="mouseover('g')"
            :style="getHoverColour('g')">
            <strong class="mr-2">Games: </strong>
            <span v-if="statcast" v-text="100"></span>
          </div>
        </v-row>
        <v-row justify="center">
          <div
            class="pa-1 stat"
            @mouseover="mouseover('ab')"
            :style="getHoverColour('ab')">
            <strong class="mr-2">At Bats: </strong>
            <span v-if="statcast" v-text="500"></span>
          </div>
        </v-row>
        <v-row justify="center">
          <div
            class="pa-1 stat"
            @mouseover="mouseover('avg')"
            :style="getHoverColour('avg')">
            <strong class="mr-2">AVG: </strong>
            <span v-if="statcast" v-text="0.001"></span>
          </div>
        </v-row>
        <v-row justify="center">
          <div
            class="pa-1 stat"
            @mouseover="mouseover('obp')"
            :style="getHoverColour('obp')">
            <strong class="mr-2">OBP: </strong>
            <span v-if="statcast" v-text="0.001"></span>
          </div>
        </v-row>
        <v-row justify="center">
          <div
            class="pa-1 stat"
            @mouseover="mouseover('ops')"
            :style="getHoverColour('ops')">
            <strong class="mr-2">OPS: </strong>
            <span v-if="statcast" v-text="0.001"></span>
          </div>
        </v-row>
      </v-col>
      <v-col cols="6">
        <v-row justify="center">
          <div
            class="pa-1 stat"
            @mouseover="mouseover('h')"
            :style="getHoverColour('h')">
            <strong class="mr-2">Hits: </strong>
            <span v-if="statcast" v-text="events.hits"></span>
          </div>
        </v-row>
        <v-row justify="center">
          <div
            class="pa-1 stat"
            @mouseover="mouseover('1b')"
            :style="getHoverColour('1b')">
            <strong class="mr-2">1B: </strong>
            <span v-if="statcast" v-text="events.single"></span>
          </div>
        </v-row>
        <v-row justify="center">
          <div
            class="pa-1 stat"
            @mouseover="mouseover('2b')"
            :style="getHoverColour('2b')">
            <strong class="mr-2">2B: </strong>
            <span v-if="statcast" v-text="events.double"></span>
          </div>
        </v-row>
        <v-row justify="center">
          <div
            class="pa-1 stat"
            @mouseover="mouseover('3b')"
            :style="getHoverColour('3b')">
            <strong class="mr-2">3B: </strong>
            <span v-if="statcast" v-text="events.triple"></span>
          </div>
        </v-row>
        <v-row justify="center">
          <div
            class="pa-1 stat"
            @mouseover="mouseover('hr')"
            :style="getHoverColour('hr')">
            <strong class="mr-2">HR: </strong>
            <span v-if="statcast" v-text="events.home_run"></span>
          </div>
        </v-row>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import { Hub } from 'aws-amplify';
import Loading from '@/components/CompareCard/Loading'

export default {
  name: 'StatsSimple',

  components: {
    Loading
  },

  props: ['statcast'],

  data() {
    return {
      selected: 'g',
      events: {
        hits: 0,
        single: 0,
        double: 0,
        triple: 0,
        home_run: 0
      }
    }
  },

  mounted() {
    this.plot();

    Hub.listen('Hover', data => {
      this.selected = data.payload.data;
    });
  },

  methods: {
    getHoverColour(stat) {
      if (stat == this.selected) {
        return 'background-color: #fff3c9';
      }
      return '';
    },
    mouseover(stat) {
      this.selected = stat;
      Hub.dispatch('Hover', {
        data : this.selected
      });
    },
    plot() {
      this.statcast.forEach(row => {
        this.events[row.events]++;
        this.events.hits++;
      });
    }
  },

  watch: {
    statcast() {
      this.plot()
    }
  }
}
</script>

<style scoped>
  .stat {
    cursor: pointer;
  }
</style>