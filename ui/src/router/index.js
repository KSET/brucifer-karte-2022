import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import Guests from '../views/GuestsView.vue'
import Tags from '../views/TagsView.vue'
import Users from '../views/UsersView.vue'
import Privileges from '../views/PrivilegesView.vue'
import Import from '../views/ImportView.vue'
import Export from '../views/ExportView.vue'
import GuestTag from '../views/GuestTagView.vue'
import Login from '../views/LoginView.vue'
import Logout from '../views/LogoutView.vue'
import store from '@/store/index.js';



const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/tags',
    name: 'tags',
    component : Tags,
  },
  {
    path: '/guests',
    name: 'guests',
    component : Guests
  },
  {
    path: '/guest_tag/:slug',
    name: 'guest_tag',
    alias: '/guest_tag/guest_tag/:slug',
    component : GuestTag
  },
  {
    path: '/users',
    name: 'users',
    component : Users
  },
  {
    path: '/privileges',
    name: 'privileges',
    component : Privileges
  },
  {
    path: '/import',
    name: 'import',
    component : Import
  }
  ,
  {
    path: '/export',
    name: 'export',
    component : Export
  },
  {
    path: '/login',
    name: 'login',
    component : Login
  },
  {
    path: '/logout',
    name: 'logout',
    component : Logout
  },
  
  
]



const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  var allowedRoutesForprivilege2= ["home","login","logout","guest_tag","",undefined]
  var allowedRoutesForprivilege3= ["home","login","logout","guests","",undefined]
  var allowedRoutesForprivilege4= ["home","login","logout","guest_tag","guests","",undefined]

  console.log("provjera auth se kao dogodila")
  console.log("---ime  ",to.name)
  if(store.state.id=='' && to.name!='login'){
    next({path: '/login'});
  }else if((store.state.privilege==0 && to.name!='login')){
    window.alert("Nažalost, nemate privilegije za pristup ovoj stranici. Pričekajte ili se javite savjetniku(?)");
    next({path: '/home'});
  }else if((store.state.privilege==2 && !allowedRoutesForprivilege2.includes(to.name))){
      window.alert("Nažalost, nemate privilegije za pristup ovoj stranici. Pričekajte ili se javite savjetniku(?)");
      next({path: '/home'});
  }else if((store.state.privilege==3 && !allowedRoutesForprivilege3.includes(to.name))){
      window.alert("Nažalost, nemate privilegije za pristup ovoj stranici. Pričekajte ili se javite savjetniku(?)");
      next({path: '/home'});
  }else if((store.state.privilege==4 && !allowedRoutesForprivilege4.includes(to.name))){
    window.alert("Nažalost, nemate privilegije za pristup ovoj stranici. Pričekajte ili se javite savjetniku(?)");
    next({path: '/home'});
  }else{
    next();
  }
})

export default router
