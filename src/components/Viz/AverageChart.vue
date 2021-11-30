<script>
import { Line } from 'vue-chartjs';

export default {
  extends: Line,

  props: ['data'],

  data() {
    return {
      dataset: {
          labels: [],
          datasets: [{
              label: 'Average',
              data: this.data,
              fill: true,
              backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
              ],
              borderColor: '#ef9a9a',
              borderWidth: 2,
              pointRadius: 0
          }]
      },
      options: {
        scales: {
          yAxes: [{
            ticks: {
              min: 0.150,
              max: 0.400,
              callback: function(value) {
                return value.toFixed(3);
              }
            },
            gridLines: {
              display: true
            }
          }],
          xAxes: [{
            type: 'time',
            gridLines: {
              display: true
            },
            time: {
              tooltipFormat: 'MMM DD, YYYY',
              unit: 'month',
              displayFormats: {'month': 'MMM'},
            }
          }],
        },
        tooltips: {
          mode: 'x-axis',
          position: 'custom',
          backgroundColor: '#9E9E9E',
          bodyFontColor: '#fff',
          titleFontColor: '#fff',
          caretSize: 0,
          callbacks: {
            label: function(tooltipItem, data) {
              var label = data.datasets[tooltipItem.datasetIndex].label || '';
              if (label) {
                label += ': ';
              }
              label += parseFloat(tooltipItem.value).toFixed(3);
              return ' ' + label;
            }
          }
        },
        legend: {
          display: true,
          labels: {
            boxWidth: 15
          }
        },
        responsive: true,
        maintainAspectRatio: false
      }
    }
  },

  methods: {
    plot() {
      this.renderChart(this.dataset, this.options);
    }
  },

  mounted () {
    this.plot();
  },

  watch: {
    data() {
      this.plot();
    }
  }
}
</script>
