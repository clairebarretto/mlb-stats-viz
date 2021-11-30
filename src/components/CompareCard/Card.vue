<template>
  <v-card v-if="meta">
    <Actionshot :meta="meta" />
    <Headshot :meta="meta" />

    <v-card-title>
      <Bio :meta="meta" />
    </v-card-title>

    <v-card-text>
      <TitleBar title="Summary" />
      <StatsSimple :statcast="statcast" />

      <TitleBar title="Season Average" />

      <TitleBar title="Spray Chart" />
      <Stadium :team="meta.TeamShort" :statcast="statcast" />

      <TitleBar title="Pitch Type" />
    </v-card-text>
  </v-card>
</template>

<script>
import { API } from 'aws-amplify';
import Actionshot from '@/components/CompareCard/Actionshot'
import Headshot from '@/components/CompareCard/Headshot'
import Bio from '@/components/CompareCard/Bio'
import Stadium from '@/components/Viz/Stadium'
import StatsSimple from '@/components/Viz/StatsSimple'
import TitleBar from '@/components/CompareCard/TitleBar'

export default {
  name: 'Card',

  props: ['id'],

  components: {
    Actionshot,
    Headshot,
    Bio,
    Stadium,
    StatsSimple,
    TitleBar
  },

  data: () => ({
    'meta': null,
    'statcast': []
  }),

  mounted() {
    const apiName = 'GetPlayer';

    API.get(apiName, `/player/${this.id}`)
      .then(response => {
        this.meta = response;
      })
      .catch(error => {
        console.log(error);
    });

    API.get(apiName, `/player/${this.id}/statcast`)
      .then(response => {
        console.log(response);
        this.statcast = response;
      })
      .catch(error => {
        console.log(error);
    });
  },
};
</script>
