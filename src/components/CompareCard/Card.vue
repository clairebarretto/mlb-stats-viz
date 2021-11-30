<template>
  <v-card>
    <v-btn
      small
      block
      dark
      color="grey darken-4 rounded-bl-0 rounded-br-0">
      Switch Player
    </v-btn>

    <div v-if="meta">
      <Actionshot :url="meta.ActionPhotoUrl" />
      <Headshot :url="meta.HeadshotPhotoUrl" />

      <v-card-title>
        <Bio :meta="meta" />
      </v-card-title>

      <v-card-text>
        <TitleBar title="Summary" />
        <StatsSimple :statcast="statcast.total" />

        <TitleBar title="Season Average" />
        <AverageChartWrapper :statcast="statcast.day" />

        <TitleBar title="Spray Chart" />
        <StadiumSprayChart :team="meta.TeamShort" :statcast="statcast.hits" />

      </v-card-text>
    </div>
    <div v-else>
      <Actionshot />

      <v-card-text>
        <Loading fill="true" />
      </v-card-text>
    </div>
  </v-card>
</template>

<script>
import { API } from 'aws-amplify';
import Actionshot from '@/components/CompareCard/Actionshot'
import AverageChartWrapper from '@/components/Viz/AverageChartWrapper'
import Bio from '@/components/CompareCard/Bio'
import Headshot from '@/components/CompareCard/Headshot'
import Loading from '@/components/CompareCard/Loading'
import StadiumSprayChart from '@/components/Viz/StadiumSprayChart'
import StatsSimple from '@/components/Viz/StatsSimple'
import TitleBar from '@/components/CompareCard/TitleBar'

export default {
  name: 'Card',

  props: ['id'],

  components: {
    Actionshot,
    AverageChartWrapper,
    Bio,
    Headshot,
    Loading,
    StadiumSprayChart,
    StatsSimple,
    TitleBar,
  },

  data: () => ({
    'meta': null,
    'statcast': {}
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
