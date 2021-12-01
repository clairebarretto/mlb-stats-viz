<template>
  <Loading v-if="!statcast" />
  <div v-else class="mt-15 mb-15">
    <v-row>
      <v-col cols="6">
        <v-row justify="center">
          <div
            class="pa-1 stat"
            @mouseover="mouseover('g')"
            :style="getHoverColour('g')">
            <strong class="mr-2">Games: </strong>
            <span>{{ statcast.g || 0 }}</span>
          </div>
        </v-row>
        <v-row justify="center">
          <div
            class="pa-1 stat"
            @mouseover="mouseover('ab')"
            :style="getHoverColour('ab')">
            <strong class="mr-2">At Bats: </strong>
            <span>{{ statcast.ab || 0 }}</span>
          </div>
        </v-row>
        <v-row justify="center">
          <div
            class="pa-1 stat"
            @mouseover="mouseover('avg')"
            :style="getHoverColour('avg')">
            <strong class="mr-2">AVG: </strong>
            <span>{{ statcast.avg || 0 }}</span>
          </div>
        </v-row>
        <v-row justify="center">
          <div
            class="pa-1 stat"
            @mouseover="mouseover('obp')"
            :style="getHoverColour('obp')">
            <strong class="mr-2">OBP: </strong>
            <span>{{ statcast.obp || 0 }}</span>
          </div>
        </v-row>
        <v-row justify="center">
          <div
            class="pa-1 stat"
            @mouseover="mouseover('ops')"
            :style="getHoverColour('ops')">
            <strong class="mr-2">OPS: </strong>
            <span>{{ statcast.ops || 0 }}</span>
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
            <span>{{ statcast.hit || 0 }}</span>
          </div>
        </v-row>
        <v-row justify="center">
          <div
            class="pa-1 stat"
            @mouseover="mouseover('1b')"
            :style="getHoverColour('1b')">
            <strong class="mr-2">1B: </strong>
            <span>{{ statcast.single || 0 }}</span>
          </div>
        </v-row>
        <v-row justify="center">
          <div
            class="pa-1 stat"
            @mouseover="mouseover('2b')"
            :style="getHoverColour('2b')">
            <strong class="mr-2">2B: </strong>
            <span>{{ statcast.double || 0 }}</span>
          </div>
        </v-row>
        <v-row justify="center">
          <div
            class="pa-1 stat"
            @mouseover="mouseover('3b')"
            :style="getHoverColour('3b')">
            <strong class="mr-2">3B: </strong>
            <span>{{ statcast.triple || 0 }}</span>
          </div>
        </v-row>
        <v-row justify="center">
          <div
            class="pa-1 stat"
            @mouseover="mouseover('hr')"
            :style="getHoverColour('hr')">
            <strong class="mr-2">HR: </strong>
            <span>{{ statcast.home_run || 0 }}</span>
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
      selected: 'avg',
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
      // this.statcast.forEach(row => {
      //   this.events[row.events]++;
      //   this.events.hits++;
      // });
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