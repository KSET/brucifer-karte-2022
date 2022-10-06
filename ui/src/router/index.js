import { createRouter, createWebHistory } from "vue-router";

/* Buckarte page Views */
import Guests from "../views/BruckarteViews/GuestsView.vue";
import EntryView from "../views/BruckarteViews/EntryView.vue";
import Login from "../views/BruckarteViews/LoginView.vue";
import Logout from "../views/BruckarteViews/LogoutView.vue";
import PageNotFound from "../views/BruckarteViews/PageNotFound.vue";

/* Admin Views */
import Tags from "../views/AdminViews/TagsView.vue";
import Users from "../views/AdminViews/UsersView.vue";
import Privileges from "../views/AdminViews/PrivilegesView.vue";
import Import from "../views/AdminViews/ImportView.vue";
import LineupList from "../views/AdminViews/LineupListView.vue";
import SponsorsList from "../views/AdminViews/SponsorsListView.vue";
import AdminPanel from "../views/AdminViews/AdminPanelView.vue";
import LineupAdd from "../views/AdminViews/LineupAddView.vue";
import SponsorsAdd from "../views/AdminViews/SponsorsAddView.vue";
import GuestAdd from "../views/AdminViews/GuestAddView.vue";
import BandKontakt from "../views/AdminViews/BandKontaktView.vue";

/* BruciWeb Views */
import Bwlineup from "../views/BruciWebViews/BWlineupView.vue";
import BWsponsors from "../views/BruciWebViews/BWsponsorsView.vue";
import Kontakt from "../views/BruciWebViews/KontaktView.vue";
import Ulaznice from "../views/BruciWebViews/UlazniceView.vue";
import Pravila from "../views/BruciWebViews/PravilaView.vue";
import Naslovnica from "../views/BruciWebViews/NaslovnicaView.vue";
import BWPageNotFound from "../views/BruciWebViews/BWPageNotFound.vue";

import SponsorsPage from "../views/BruciWebViews/SponsorsPageView.vue";


import store from "@/store/index.js";

const routes = [
  {
    path: "/admin/",
    name: "home",
  },

  /* Bruckarte Views setup */
  {
    path: "/admin/tags",
    name: "tags",
    component: Tags,
  },
  {
    path: "/admin/guests",
    name: "guests",
    component: Guests,
  },
  {
    path: "/admin/entry",
    name: "entry",
    component: EntryView,
  },
  {
    path: "/admin/users",
    name: "users",
    component: Users,
  },
  {
    path: "/admin/privileges",
    name: "privileges",
    component: Privileges,
  },
  {
    path: "/admin/import",
    name: "import",
    component: Import,
  },
  {
    path: "/admin/login",
    name: "login",
    component: Login,
  },
  {
    path: "/admin/logout",
    name: "logout",
    component: Logout,
  },
  {
    path: "/admin/lineup-list",
    name: "lineup",
    component: LineupList,
  },
  {
    path: "/admin/sponsors/:slug",
    name: "sponsors",
    component: SponsorsList,
  },
  {
    path: "/admin/sponsors-list",
    name: "sponsors",
    component: SponsorsList,
  },
  {
    path: "/admin/guests-add",
    name: "guest-add",
    component: GuestAdd,
  },
  {
    path: "/admin/admin-panel",
    name: "admin-panel",
    component: AdminPanel,
  },
  {
    path: "/admin/lineup-add/:slug",
    name: "lineup-add",
    component: LineupAdd,
  },
  {
    path: "/admin/sponsors-add/:slug",
    name: "sponsors-add",
    component: SponsorsAdd,
  },
  {
    path: "/admin/band-kontakt",
    name: "band-kontakt",
    component: BandKontakt,
  },
  {
    path: "/admin/page-not-found",
    name: "PageNotFound",
    component: PageNotFound,
  },

  /* Brucweb Views setup */
  {
    path: "/sponsors",
    name: "bwsponsors",
    component: BWsponsors,
  },
  {
    path: "/lineup",
    name: "bwlineup",
    component: Bwlineup,
  },
  {
    path: "/kontakt",
    name: "kontakt",
    component: Kontakt,
  },
  {
    path: "/ulaznice",
    name: "ulaznice",
    component: Ulaznice,
  },
  {
    path: "/pravila-ponasanja",
    name: "pravila-ponasanja",
    component: Pravila,
  },
  {
    path: "/",
    name: "naslovnica",
    component: Naslovnica,
  },
  { path: "/:pathMatch(.*)*", component: BWPageNotFound },

  {
    path: "/sponzori/:slug",
    name: "sponzori-page",
    component: SponsorsPage,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

router.beforeEach((to, from, next) => {
  //provjera auth i privilegija
  var allowedRoutesForprivilege2 = [
    "home",
    "login",
    "logout",
    "entry",
    "",
    undefined,
    "admin",
  ];
  var allowedRoutesForprivilege3 = [
    "home",
    "login",
    "logout",
    "guests",
    "",
    undefined,
  ];
  var allowedRoutesForprivilege4 = [
    "home",
    "login",
    "logout",
    "guest_tag",
    "guests",
    "",
    undefined,
  ];

  if (String(to.path).split("/")[1] == "admin") {
    if (Date.now() / 1000 > store.state.tokenExp && to.name != "logout") {
      next({ path: "/admin/logout" });
    } else {
      if (store.state.id == "" && to.name != "login") {
        next({ path: "/admin/login" });
      } else if (store.state.privilege == 0 && to.name != "login") {
        window.alert(
          "Nažalost, nemate privilegije za pristup ovoj stranici. Pričekajte ili se javite savjetniku"
        );
        next({ path: "/admin/login" });
      } else if (
        store.state.privilege == 2 &&
        !allowedRoutesForprivilege2.includes(to.name)
      ) {
        window.alert(
          "Nažalost, nemate privilegije za pristup ovoj stranici. Pričekajte ili se javite savjetniku"
        );
        next({ path: "/admin/home" });
      } else if (
        store.state.privilege == 3 &&
        !allowedRoutesForprivilege3.includes(to.name)
      ) {
        window.alert(
          "Nažalost, nemate privilegije za pristup ovoj stranici. Pričekajte ili se javite savjetniku"
        );
        next({ path: "/admin/home" });
      } else if (
        store.state.privilege == 4 &&
        !allowedRoutesForprivilege4.includes(to.name)
      ) {
        window.alert(
          "Nažalost, nemate privilegije za pristup ovoj stranici. Pričekajte ili se javite savjetniku"
        );
        next({ path: "/admin/home" });
      } else {
        next();
      }
    }
  } else {
    next();
  }
});

export default router;
