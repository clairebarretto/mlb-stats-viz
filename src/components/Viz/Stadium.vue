<template>
  <div class="text-center">
    <svg
      :viewBox="getViewport()"
      height="100%"
      width="80%"
      class="stadium"
      xmlns="http://www.w3.org/2000/svg">

      <!-- Stadium outline -->
      <polygon class="outfield_outer" :points="locations.outfield_outer" />
      <polygon class="outfield_inner" :points="locations.outfield_inner" />
      <polyline class="foul_lines" :points="locations.foul_lines" />
      <polygon class="infield_outer" :points="locations.infield_outer" />
      <polygon class="infield_inner" :points="locations.infield_inner" />
      <polygon class="home_plate" :points="locations.home_plate" />

      <StadiumHit v-for="(row, index) in hits" :key="index" v-bind:hit="row" />
    </svg>
  </div>
</template>

<script>
import { API } from 'aws-amplify';
import StadiumHit from "@/components/Viz/StadiumHit";

export default {
    components: {
      StadiumHit
    },
    props: ['statcast', 'team'],
    data() {
      return {
        width: 250,
        height: 250,
        hits: [],
        locations: {
          infield_inner: [],
          infield_outer: [],
          outfield_outer: [],
          outfield_inner: [],
          foul_lines: [],
          home_plate: []
        }
      }
    },
    methods: {
      getStadiumDimensions() {
        const apiName = 'GetStadiumDimensions';
        const path = `/team/${this.team}/stadium`;

        API.get(apiName, path)
          .then(response => {
            response.forEach(row => {
              this.locations[row.Segment].push(`${row.X},${row.Y}`);
            });
            Object.keys(this.locations).map(key => {
              this.locations[key] = this.locations[key].join(' ');
            });
          })
          .catch(error => {
            console.log(error);
        });
      },
      getViewport() {
        return `0 0 ${this.width} ${this.height}`;
      },
      plot() {
        const result = [];
        this.statcast.forEach((row) => {
          if (row.hc_x > 0 && row.hc_y > 0) {
            result.push(row);
          }
        });
        this.hits = result;
      }
    },
    mounted () {
      this.getStadiumDimensions();
      this.plot();
    },
    watch: {
      statcast() {
        this.plot()
      }
    }
}
</script>

<style lang="postcss" scoped>
  .outfield_outer,
  .infield_outer {
    fill: #a98c48;
    stroke: #a98c48;
    stroke-width: 1
  }

  .outfield_inner,
  .infield_inner {
    fill: #68836a;
    stroke: #68836a;
    stroke-width: 1;
  }

  .foul_lines {
    fill: none;
    stroke: #fff;
    stroke-width: 0.3;
  }

  .home_plate {
    fill: #fff;
    stroke: #fff;
    stroke-width: 1
  }

  .tracking_line {
    stroke: #444;
    stroke-dasharray: 1;
  }
</style>