import Vue from 'vue'
import Amplify from 'aws-amplify';
import App from './App.vue'
import vuetify from './plugins/vuetify'
import aws_config from './aws-exports';
import {
    applyPolyfills,
    defineCustomElements,
} from '@aws-amplify/ui-components/loader';

Amplify.configure(aws_config);

applyPolyfills().then(() => {
    defineCustomElements(window);
});

Vue.config.productionTip = false

new Vue({
  vuetify,
  render: h => h(App)
}).$mount('#app');