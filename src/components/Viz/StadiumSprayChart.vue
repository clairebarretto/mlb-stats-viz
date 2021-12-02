<template>
  <Loading v-if="!statcast || !ballpark_home.outfield_inner.length" />
  <div v-else class="text-center">
    <v-row class="ml-5 mr-5 mb-1">
      <v-col cols="6">
        <StadiumLocationFilter :location_type="location_type" />
      </v-col>
      <v-col cols="6">
        <StadiumPitcherFilter :pitcher_type="pitcher_type" />
      </v-col>
    </v-row>
    <svg
      :viewBox="getViewport()"
      height="100%"
      width="80%"
      class="stadium"
      xmlns="http://www.w3.org/2000/svg">

      <polygon class="outfield_outer" :points="ballpark.outfield_outer" />
      <polygon class="outfield_inner" :points="ballpark.outfield_inner" />
      <polyline class="foul_lines" :points="ballpark.foul_lines" />
      <polygon class="infield_outer" :points="ballpark.infield_outer" />
      <polygon class="infield_inner" :points="ballpark.infield_inner" />
      <polygon class="home_plate" :points="ballpark.home_plate" />

      <StadiumHit v-for="(row, index) in hits" :key="index" v-bind:hit="row" />
    </svg>
    <StadiumHitFilter :filters="hit_events" />
    <br/>
    <br/>
    <div class="text-center">
      <small>{{ location_type == 'away' ? 'AWAY' : 'HOME'}} FIELD</small>
      <br/>
      <strong>{{ ballpark.stadium }}</strong>
      <br/>
      {{ ballpark.city }}
    </div>
  </div>
</template>

<script>
import { API, Hub } from 'aws-amplify';
import Loading from '@/components/CompareCard/Loading'
import StadiumHit from "@/components/Viz/StadiumHit";
import StadiumHitFilter from "@/components/VizFilter/StadiumHitFilter";
import StadiumLocationFilter from "@/components/VizFilter/StadiumLocationFilter";
import StadiumPitcherFilter from "@/components/VizFilter/StadiumPitcherFilter";

export default {
  components: {
    Loading,
    StadiumHit,
    StadiumHitFilter,
    StadiumLocationFilter,
    StadiumPitcherFilter,
  },
  props: ['statcast', 'team'],
  data() {
    return {
      hit_events: ['single', 'double', 'triple', 'home_run'],
      location_type: 'both',
      pitcher_type: 'both',
      width: 250,
      height: 250,
      hits: [],
      stadium: '',
      city: '',
      ballpark_home: {
        infield_inner: [],
        infield_outer: [],
        outfield_outer: [],
        outfield_inner: [],
        foul_lines: [],
        home_plate: [],
        stadium: '',
        city: ''
      },
      ballpark_away: {
        infield_inner: [],
        infield_outer: [],
        outfield_outer: [],
        outfield_inner: [],
        foul_lines: [],
        home_plate: [],
        stadium: 'MLB Ballpark',
        city: 'Anywhere, USA'
      },
      ballpark: {}
    }
  },
  methods: {
    getStadiumDimensions() {
      API.get('GetStadiumDimensions', `/team/${this.team}/stadium`)
        .then(response => {
          response.forEach(row => {
            this.ballpark_home[row.Segment].push(`${row.X},${row.Y}`);
            this.ballpark_home.stadium = row.Name;
            this.ballpark_home.city = row.Location;
          });
          Object.keys(this.ballpark_home).map(key => {
            if (Array.isArray(this.ballpark_home[key])) {
              this.ballpark_home[key] = this.ballpark_home[key].join(' ');
            }
          });
          this.ballpark = this.ballpark_home;
        })
        .catch(error => {
          console.log(error);
      });
      API.get('GetStadiumDimensions', `/team/cws/stadium`)
        .then(response => {
          response.forEach(row => {
            this.ballpark_away[row.Segment].push(`${row.X},${row.Y}`);
          });
          Object.keys(this.ballpark_away).map(key => {
            if (Array.isArray(this.ballpark_away[key])) {
              this.ballpark_away[key] = this.ballpark_away[key].join(' ');
            }
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
      if (!this.statcast) {
        return result;
      }
      this.statcast.forEach((row) => {
        if (!row.hc_x || !row.hc_y) {
          return;
        }
        if (!this.hit_events.includes(row.events)) {
          return;
        }
        if (this.location_type == 'home' && row.home_team != this.team) {
          return;
        }
        if (this.location_type == 'away' && row.home_team == this.team) {
          return;
        }
        if (this.pitcher_type == 'L' && row.p_throws != 'L') {
          return;
        }
        if (this.pitcher_type == 'R' && row.p_throws != 'R') {
          return;
        }
        result.push(row);
      });
      this.hits = result;
    }
  },
  mounted () {
    this.getStadiumDimensions();
    this.plot();

    Hub.listen('StadiumHitFilter', data => {
      if (this.hit_events != data.payload.data) {
        this.hit_events = data.payload.data;
        this.plot();
      }
    });
    Hub.listen('StadiumLocationFilter', data => {
      if (this.location_type != data.payload.data) {
        this.location_type = data.payload.data;
        if (this.location_type == 'away') {
          this.ballpark = this.ballpark_away;
          console.log(this.location_type)
        } else {
          this.ballpark = this.ballpark_home;
        }
        this.plot();
      }
    });
    Hub.listen('StadiumPitcherFilter', data => {
      if (this.pitcher_type != data.payload.data) {
        this.pitcher_type = data.payload.data;
        this.plot();
      }
    });
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

  .v-select {
    font-size: 90%;
  }
</style>