import { createRouter, createWebHistory } from 'vue-router'

/* Buckarte page Views */
import Guests from '../views/BruckarteViews/GuestsView.vue'
import EntryView from '../views/BruckarteViews/EntryView.vue'
import Login from '../views/BruckarteViews/LoginView.vue'
import Logout from '../views/BruckarteViews/LogoutView.vue'


/* Admin Views */
import Tags from '../views/AdminViews/TagsView.vue'
import Users from '../views/AdminViews/UsersView.vue'
import Privileges from '../views/AdminViews/PrivilegesView.vue'
import Import from '../views/AdminViews/ImportView.vue'
import Export from '../views/AdminViews/ExportView.vue'
import LineupList from '../views/AdminViews/LineupListView.vue'
import SponsorsList from '../views/AdminViews/SponsorsListView.vue'
import AdminPanel from '../views/AdminViews/AdminPanelView.vue'
import LineupAdd from '../views/AdminViews/LineupAddView.vue'
import SponsorsAdd from '../views/AdminViews/SponsorsAddView.vue'
import GuestAdd from '../views/AdminViews/GuestAddView.vue'

/* BruciWeb Views */
import Bwlineup from '../views/BruciWebViews/BWlineupView.vue'
import BWsponsors from '../views/BruciWebViews/BWsponsorsView.vue'
import Kontakt from '../views/BruciWebViews/KontaktView.vue'
import Ulaznice from '../views/BruciWebViews/UlazniceView.vue'
import Pravila from '../views/BruciWebViews/PravilaView.vue'
import Naslovnica from '../views/BruciWebViews/NaslovnicaView.vue'
import Upis from '../views/BruciWebViews/UpisView.vue'

import store from '@/store/index.js';



const routes = [
  {
    path: '/bruckarte/',
    name: 'home',
  },

  /* Bruckarte Views setup */
  {
    path: '/bruckarte/tags',
    name: 'tags',
    component : Tags,
  },
  {
    path: '/bruckarte/guests',
    name: 'guests',
    component : Guests
  },
  {
    path: '/bruckarte/entry',
    name: 'guest_tag',
    component : EntryView
  },
  {
    path: '/bruckarte/users',
    name: 'users',
    component : Users
  },
  {
    path: '/bruckarte/privileges',
    name: 'privileges',
    component : Privileges
  },
  {
    path: '/bruckarte/import',
    name: 'import',
    component : Import
  }
  ,
  {
    path: '/bruckarte/export',
    name: 'export',
    component : Export
  },
  {
    path: '/bruckarte/login',
    name: 'login',
    component : Login
  },
  {
    path: '/bruckarte/logout',
    name: 'logout',
    component : Logout
  },
  {
    path: '/bruckarte/lineup-list',
    name: 'lineup',
    component : LineupList
  },
  {
    path: '/bruckarte/sponsors/:slug',
    name: 'sponsors',
    component : SponsorsList
  },
  {
    path: '/bruckarte/sponsors-list',
    name: 'sponsors',
    component : SponsorsList
  },
  {
    path: '/bruckarte/guests-add',
    name: 'guest-add',
    component : GuestAdd
  },
  {
    path: '/bruckarte/admin-panel',
    name: 'admin-panel',
    component : AdminPanel
  },
  {
    path: '/bruckarte/lineup-add/:slug',
    name: 'lineup-add',
    component : LineupAdd
  },
  {
    path: '/bruckarte/sponsors-add/:slug',
    name: 'sponsors-add',
    component : SponsorsAdd
  },
  
  /* Brucweb Views setup */
  {
    path: '/sponsors',
    name: 'bwsponsors',
    component : BWsponsors
  },
  {
    path: '/lineup',
    name: 'bwlineup',
    component : Bwlineup
  },
  {
    path: '/kontakt',
    name: 'kontakt',
    component : Kontakt
  },
  {
    path: '/ulaznice',
    name: 'ulaznice',
    component : Ulaznice
  },
  {
    path: '/pravila-ponasanja',
    name: 'pravila-ponasanja',
    component : Pravila
  },
  {
    path: '/',
    name: 'naslovnica',
    component : Naslovnica
  },
  {
    path: '/upis',
    name: 'upis',
    component : Upis
  },
  
  
  
]



const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  
  //provjera auth i privilegija
  var allowedRoutesForprivilege2= ["home","login","logout","guest_tag","",undefined,"bruckarte"]
  var allowedRoutesForprivilege3= ["home","login","logout","guests","",undefined]
  var allowedRoutesForprivilege4= ["home","login","logout","guest_tag","guests","",undefined]

  
  if((String(to.path).split("/"))[1]=="bruckarte"){
    if((Date.now()/1000)>store.state.tokenExp && to.name!='logout'){
      next({path: '/bruckarte/logout'});
    }else{
    if(store.state.id=='' && to.name!='login'){
      next({path: '/bruckarte/login'});
    }else if((store.state.privilege==0 && to.name!='login')){
      window.alert("Nažalost, nemate privilegije za pristup ovoj stranici. Pričekajte ili se javite savjetniku");
      next({path: '/bruckarte/login'});
    }else if((store.state.privilege==2 && !allowedRoutesForprivilege2.includes(to.name))){
        window.alert("Nažalost, nemate privilegije za pristup ovoj stranici. Pričekajte ili se javite savjetniku");
        next({path: '/bruckarte/home'});
    }else if((store.state.privilege==3 && !allowedRoutesForprivilege3.includes(to.name))){
        window.alert("Nažalost, nemate privilegije za pristup ovoj stranici. Pričekajte ili se javite savjetniku");
        next({path: '/bruckarte/home'});
    }else if((store.state.privilege==4 && !allowedRoutesForprivilege4.includes(to.name))){
      window.alert("Nažalost, nemate privilegije za pristup ovoj stranici. Pričekajte ili se javite savjetniku");
      next({path: '/bruckarte/home'});
    }else{
      next();
    }}
  }else{
    next();
  }
  
})

export default router
