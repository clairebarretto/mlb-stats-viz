<template>
  <Loading v-if="!statcast" />
  <AverageChart v-else class="chart" :data="chartData" />
</template>
<script>
import AverageChart from "@/components/Viz/AverageChart";
import Loading from "@/components/CompareCard/Loading";

export default {
  name: 'AvergeChartWrapper',
  props: ['statcast'],
  components: {
      AverageChart,
      Loading
  },
  data () {
    return {
        chartData: []
    }
  },
  methods: {
    plot() {
      if (this.statcast) {
        this.chartData = [];

        let hits = 0;
        let ab = 0;

        Object.keys(this.statcast).sort().forEach(date => {
          const row = this.statcast[date];
          hits += row.hit;
          ab += row.ab;

          let avg = 0;
          if (ab) {
            avg = (hits / ab).toFixed(3);
          }

          this.chartData.push({
            x: new Date(date),
            y: avg
          })
        });
      }
    }
  },
  mounted () {
    this.plot();
  },
  watch: {
    statcast: function() {
        this.plot();
    }
  }
}
</script>
<style>
    .chart {
        height: 225px;
    }
</style>
