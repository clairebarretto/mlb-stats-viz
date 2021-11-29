<template>
  <g>
    <circle
        v-bind:cx="hit.hc_x"
        v-bind:cy="hit.hc_y"
        r="3"
        :stroke="getStrokeColour"
        stroke-width="0.6"
        :fill="getHitColour" />
  </g>
</template>

<script>
export default {
  name: 'StadiumHit',

  props: ['hit'],

  computed: {
    getHitColour() {
      switch (this.hit.events) {
        case 'home_run':
          return '#B39DDB';

        case 'single':
          return '#81c784';

        case 'triple':
          return '#ffca28';

        case 'double':
          return '#e33371';
      }
      return 'transparent';
    },
    getStrokeColour() {
      switch (this.hit.events) {
        case 'home_run':
          return '#5E35B1';

        case 'single':
          return '#388e3c';

        case 'triple':
          return '#ffa000';

        case 'double':
          return '#9a0036';
      }
      return 'transparent';
    }
  }
}
</script>