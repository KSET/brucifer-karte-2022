import { createApp, Vue } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css'
import 'jquery/src/jquery.js'
import 'bootstrap/dist/js/bootstrap.min.js';
import JsonCSV from 'vue-json-csv';
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import VueJwtDecode from 'vue-jwt-decode'
import Vuex from 'vuex';
import VueNavigationBar from 'vue-navigation-bar';
import 'vue-navigation-bar/dist/vue-navigation-bar.css';
import "./../node_modules/bulma/css/bulma.css";
import VueCountdown from '@chenfengyuan/vue-countdown';
import UUID from 'vue-uuid'  


const app= createApp(App).use(store).use(router)


app.component('downloadCsv', JsonCSV).component('VueJwtDecode', VueJwtDecode);
app.component(VueCountdown.name, VueCountdown);

app.use(Vuex)
app.use(UUID)

import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

const customTheme = {
  dark: false,
  colors: {
    background: '#FFFFFF',
    surface: '#FFFFFF',
    primary: 'black',
    'primary-darken-1': 'black',
    secondary: 'black',
    'secondary-darken-1': 'black',
    error: 'black',
    info: 'black',
    success: 'black',
    warning: 'black',
  },
}

const vuetify = createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: 'customTheme',
    themes: {
      customTheme,
    },
  },
})

app.use(vuetify)

import QrcodeStream from "vue-qrcode-reader";
import VueQrcodeReader from "vue-qrcode-reader";

app.use(VueQrcodeReader)
app.component('QrcodeStream', QrcodeStream);


app.component('VueNavigationBar', VueNavigationBar);

import { library } from '@fortawesome/fontawesome-svg-core'

/* import font awesome icon component */
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

/* import specific icons */
import { faTrashCan, faCheck, faXmark } from '@fortawesome/free-solid-svg-icons'

/* add icons to the library */
library.add(faTrashCan)
library.add(faCheck)
library.add(faXmark)


app.component('font-awesome-icon', FontAwesomeIcon)
app.mount('#app')


