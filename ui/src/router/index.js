import { createRouter, createWebHistory } from "vue-router";
import visibilityStore from "@/store/visibilityStore.js";
import store from "@/store/index.js";

/* Buckarte page Views */
import Guests from "../views/BruckarteViews/GuestsView.vue";
import EntryView from "../views/BruckarteViews/EntryView.vue";
import Login from "../views/BruckarteViews/LoginView.vue";
import Logout from "../views/BruckarteViews/LogoutView.vue";
import PageNotFound from "../views/BruckarteViews/PageNotFound.vue";

/* Admin Views */
import Tags from "../views/AdminViews/TagsView.vue";
import Users from "../views/AdminViews/UsersView.vue";
import UsersAdd from "../views/AdminViews/UsersAddView.vue";
import Privileges from "../views/AdminViews/PrivilegesView.vue";
import Import from "../views/AdminViews/ImportView.vue";
import LineupList from "../views/AdminViews/LineupListView.vue";
import SponsorsList from "../views/AdminViews/SponsorsListView.vue";
import AdminPanel from "../views/AdminViews/AdminPanelView.vue";
import LineupAdd from "../views/AdminViews/LineupAddView.vue";
import SponsorsAdd from "../views/AdminViews/SponsorsAddView.vue";
import GuestAdd from "../views/AdminViews/GuestAddView.vue";
import BandKontakt from "../views/AdminViews/BandKontaktView.vue";
import Firme from "../views/AdminViews/FirmeView.vue";
import Cjenik from "../views/AdminViews/CjenikView.vue";
import Visibility from "../views/AdminViews/VisibilityView.vue";
import Translations from "../views/AdminViews/TranslationsView.vue";
import DailyReport from "../views/AdminViews/DailyReportView.vue";

/* BruciWeb Views */
import Bwlineup from "../views/BruciWebViews/BWlineupView.vue";
import BWsponsors from "../views/BruciWebViews/BWsponsorsView.vue";
import Kontakt from "../views/BruciWebViews/KontaktView.vue";
import Ulaznice from "../views/BruciWebViews/UlazniceView.vue";
import Pravila from "../views/BruciWebViews/PravilaView.vue";
import Naslovnica from "../views/BruciWebViews/NaslovnicaView.vue";
import BWPageNotFound from "../views/BruciWebViews/BWPageNotFound.vue";
import BWcjenik from "../views/BruciWebViews/BWcjenikView.vue";
import Tlocrt from "../views/BruciWebViews/TlocrtView.vue";
import Satnica from "../views/BruciWebViews/SatnicaView.vue";
import Igrica from "../views/BruciWebViews/IgricaView.vue";
import UvjetiKoristenja from "../views/BruciWebViews/UvjetiKoristenjaView.vue";

import SponsorsPage from "../views/BruciWebViews/SponsorsPageView.vue";

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
    path: "/admin/users-add",
    name: "usersAdd",
    component: UsersAdd,
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
    path: "/admin/firme",
    name: "firme",
    component: Firme,
  },
  {
    path: "/admin/cjenik",
    name: "cjenik",
    component: Cjenik,
  },
  {
    path: "/admin/visibility",
    name: "visibility",
    component: Visibility,
  },
  {
    path: "/admin/translations",
    name: "translations",
    component: Translations,
  },
  {
    path: "/admin/daily-report",
    name: "dailyReport",
    component: DailyReport,
  },
  {
    path: "/admin/:pathMatch(.*)*",
    name: "PageNotFound",
    component: PageNotFound,
  },

  /* Brucweb Views setup */
  {
    path: "/sponsors",
    name: "bwsponsors",
    component: BWsponsors,
    meta: {
      visibilityCheck: "SPONSORS_VISIBILITY",
    },
  },
  {
    path: "/lineup",
    name: "bwlineup",
    component: Bwlineup,
    meta: {
      visibilityCheck: "LINEUP_VISIBILITY",
    },
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
    meta: {
      visibilityCheck: "ULAZNICA_VISIBILITY",
    },
  },
  {
    path: "/pravila-ponasanja",
    name: "pravila-ponasanja",
    component: Pravila,
  },
  {
    path: "/uvjeti-koristenja",
    name: "uvjeti-koristenja",
    component: UvjetiKoristenja,
    meta: {
      visibilityCheck: "IGRICA_VISIBILITY",
    },
  },
  {
    path: "/cjenik",
    name: "BWcjenik",
    component: BWcjenik,
    meta: {
      visibilityCheck: "CJENIK_VISIBILITY",
    },
  },
  {
    path: "/tlocrt",
    name: "Tlocrt",
    component: Tlocrt,
    meta: {
      visibilityCheck: "TLOCRT_VISIBILITY",
    },
  },
  {
    path: "/Satnica",
    name: "satnica",
    component: Satnica,
    meta: {
      visibilityCheck: "SATNICA_VISIBILITY",
    },
  },
  {
    path: "/igrica",
    name: "igrica",
    component: Igrica,
    meta: {
      visibilityCheck: "IGRICA_VISIBILITY",
    },
  },
  {
    path: "/",
    name: "naslovnica",
    component: Naslovnica,
  },
  {
    path: "/:pathMatch(.*)*",
    name: "BWPageNotFound",
    component: BWPageNotFound,
  },

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
    "entry",
    "",
    undefined,
  ];

  if (to.path.startsWith("/admin")) {
    if (Date.now() / 1000 > store.state.tokenExp && to.name !== "logout") {
      next({ path: "/admin/logout" });
    } else if (store.state.id === "" && to.name !== "login") {
      next({ path: "/admin/login" });
    } else if (store.state.privilege == 0 && to.name !== "login") {
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
      next({ path: "/admin" });
    } else if (
      store.state.privilege == 3 &&
      !allowedRoutesForprivilege3.includes(to.name)
    ) {
      window.alert(
        "Nažalost, nemate privilegije za pristup ovoj stranici. Pričekajte ili se javite savjetniku"
      );
      next({ path: "/admin" });
    } else if (
      store.state.privilege == 4 &&
      !allowedRoutesForprivilege4.includes(to.name)
    ) {
      window.alert(
        "Nažalost, nemate privilegije za pristup ovoj stranici. Pričekajte ili se javite savjetniku"
      );
      next({ path: "/admin" });
    } else {
      next();
    }
  } else {
    next();
  }
});

router.beforeEach((to, from, next) => {
  /* check when coming soon is visible */
  if (
    !to.path.includes("admin") &&
    to.name !== "naslovnica" &&
    to.name !== "BWPageNotFound"
  ) {
    if (visibilityStore.state.COMINGSOON_VISIBILITY == 1) {
      next({ name: "BWPageNotFound" });
    } else {
      next();
    }
  } else {
    next();
  }
});

router.beforeEach((to, from, next) => {
  /* check if page is visible */
  if (!to.path.includes("admin")) {
    if (to.meta.visibilityCheck != undefined) {
      if (store.state[to.meta.visibilityCheck] == 0) {
        next({ name: "BWPageNotFound" });
      } else {
        next();
      }
    } else {
      next();
    }
  } else {
    next();
  }
});

export default router;
