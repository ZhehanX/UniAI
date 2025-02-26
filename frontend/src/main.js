import './assets/style.css'
import { createApp } from 'vue'
import App from './App.vue'
import HighchartsVue from "highcharts-vue";
import Highcharts from "highcharts";
import router from './router';

Highcharts.setOptions({
    lang: {
      decimalPoint: ".",
      thousandsSep: ",",
    },
  });

const app = createApp(App)

app.use(HighchartsVue)
app.use(router)
app.mount('#app')