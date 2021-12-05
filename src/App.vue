<template>
  <v-app>
    <Header/>
    <v-container fluid grey lighten-5 class="pa-5">
        <Compare/>
    </v-container>
  </v-app>
</template>

<script>
import Compare from '@/views/Compare';
import Header from '@/components/Header';

export default {
  name: 'App',
  components: {
    Compare,
    Header
  }
};
</script>
