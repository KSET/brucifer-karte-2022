<template>
  <div class="users">
    <Sidebar />
    <div class="admin-page-container" :class="$style.flexi">
      <div class="page-header user-page">
        <h1 class="page-title user-title">Korisnici</h1>
        <router-link class="icon7" to="/admin/users-add">
          <img style="width: 40px; height: 40px;" src="../../assets/icons/add-icon.svg">
        </router-link>
        <input @input="searchUser" type="text" class="nosubmit search users" placeholder="Unesi ime/prezime/email"
          v-model="search" style="display: inline-block; margin-top: 0px; position: relative;">
      </div>
      <div class=row>
        <table id="guests">
          <tbody>
            <div class="users-container" v-for="user in users" :key="user.id">
              <div class="users-element hideDesktop hideTablett showMobile"><button class="button-priv"
                  style="border: none; opacity: 0.25;" @click="deleteUser(user)">
                  <img src="@/assets/icons/trash-icon.svg"></button></div>
              <div class="users-element userinfo" style="flex: 2;"
                v-bind:style="[(user.privilege == '0') ? { color: 'red' } : { color: 'black' }]">{{ user.name }} <br>
                {{ user.email }}</div>
              <div class="users-element"> <button class="button-priv"
                  v-bind:style="[(user.privilege == '3') ? { backgroundColor: 'black', color: 'white' } : { backgroundColor: 'white', color: 'black' }]"
                  @click="changeprivilege(user, '3')">Karte</button></div>
              <div class="users-element"><button class="button-priv"
                  v-bind:style="[(user.privilege == '2') ? { backgroundColor: 'black', color: 'white' } : { backgroundColor: 'white', color: 'black' }]"
                  @click="changeprivilege(user, '2')">Ulaz</button></div>
              <div class="users-element"><button class="button-priv"
                  v-bind:style="[(user.privilege == '4') ? { backgroundColor: 'black', color: 'white' } : { backgroundColor: 'white', color: 'black' }]"
                  @click="changeprivilege(user, '4')">Ulaz <br>+Karte</button></div>
              <div class="users-element"><button class="button-priv"
                  v-bind:style="[(user.privilege == '1') ? { backgroundColor: 'black', color: 'white' } : { backgroundColor: 'white', color: 'black' }]"
                  @click="changeprivilege(user, '1')">Admin</button></div>



              <div class="users-element hideMobile"><button class="button-priv" style="border:0px"
                  @click="deleteUser(user)">
                  <img src="@/assets/icons/trash-icon.svg">
                </button>
              </div>
            </div>
          </tbody>
        </table>


      </div>
    </div>
  </div>
</template>

<style module lang="scss">
:global(#app) .flexi {
  display: flex;
  flex-direction: column;

  :global(.row) {
    overflow: scroll;
    flex: 1;

    tbody {
      height: initial;
    }
  }
}
</style>

<script>
import Sidebar from '@/components/NavbarAndFooter/Sidebar.vue'
import { api } from "@/plugins/api";
export default {
  name: 'UsersView',
  components: {
    Sidebar
  },
  data() {
    return {
      users: [],
      mails: [],
      id: '',
      name: '',
      email: '',
      privilege: '',
    }

  },
  mounted() {
    this.created();
  },

  methods: {
    created() {
      api.get(process.env.VUE_APP_BASE_URL + '/users/',)
        .then(response => {
          this.users = response.data;
        })
    },
    changeprivilege(user, changenum) {
      api.put(process.env.VUE_APP_BASE_URL + '/users/' + user.id + '/',
        { privilege: changenum },
      )
        .then(() => {
          this.sendMail(user, changenum);
          this.created();
        })
    },
    deleteUser(user) {
      api.delete(process.env.VUE_APP_BASE_URL + '/users/' + user.id + '/',
      )
        .then(() => {
          this.sendMail(user, 0);
          this.created();
        })
    },
    searchUser() {
      api.get(process.env.VUE_APP_BASE_URL + '/users/?search=' + this.search,)
        .then(response => {
          this.users = response.data;
        })
    },
    async sendMail(user, changenum) {
      console.log("send mail attempt")

      var privilege_name = 0;
      if (changenum == 1) {
        privilege_name = "Admin";
      } else if (changenum == 3) {
        privilege_name = "Karte";
      } else if (changenum == 2) {
        privilege_name = "Ulaz";
      } else if (changenum == 4) {
        privilege_name = "Ulaz+Karte";
      }
      else if (changenum == 0) {
        privilege_name = "Ništa- nažalost, tvoj pristup stranici je obustavljen";
      }

      var to_user_name = user.name.split(" ")[0];

      var email = user.email

      // await api.post(process.env.VUE_APP_BASE_URL + '/mailer/send_mail/',
      //   {
      //     emails:
      //       [{
      //         subject: "[#BRUCIFER25] Promjena privilegije",
      //         template: "user_email",
      //         message: user.name + " " + privilege_name,
      //         name: to_user_name,
      //         privilege_name: privilege_name,
      //         to_mail: email
      //       }]
      //   },
      //   { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } }
      // )

      // await api.post(process.env.VUE_APP_BASE_URL + '/mailer/',
      //   {
      //     subject: "[#BRUCIFER25] Promjena privilegije",
      //     template: "user_email",
      //     message: user.name + " " + privilege_name,
      //     name: to_user_name,
      //     privilege_name: privilege_name,
      //     to_mail: email
      //   },
      //   { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } }
      // )

      this.created();
    }
  }

}


</script>


<style >
.page-header.user-page {
  border-bottom: 0.5px solid black;
}

.page-title.user-title {
  padding-right: 1%;
  vertical-align: middle;
}

.nosubmit.search.users {
  width: 25% !important;
}

.user-search {
  padding-left: 40px;
  margin-left: 7%;
  width: 35%;
  height: 40px;
  vertical-align: middle;
  height: 40px;
  font-family: 'Montserrat';
  font-size: 16px;

}

.add-icon.user-icon {
  vertical-align: middle;
}

.search-icon {
  position: absolute;
  top: 8.4%;
  left: 24.7%;
}


.button-priv {
  position: relative;
  border: 0.5px solid black;
  background-color: white;
  height: 70px;
  width: 70px;

}

.users-element {

  border: 0px;
  border-bottom: 0.5px solid black;
  padding: 8px;
  text-align: left;
  vertical-align: middle;
  font-family: 'Montserrat';
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: left;
  font-size: 16px;
  flex: 1;
}

.users-container {
  display: flex;
  flex-direction: row;
  align-items: stretch !important;
  width: 100%;
  padding-top: 12px;
  padding-bottom: 12px;
  text-align: left;
  background-color: white;
  color: black;
}

@media screen and (max-width: 980px) {
  .hideTablett {
    display: none !important;
  }

  .nosubmit.search.users {
    width: 35% !important;
  }
}

@media screen and (max-width: 550px) {
  .users-container {
    display: grid !important;
    grid-template-columns: repeat(4, 1fr);
  }

  .button-priv {

    height: 38px;
    width: 38px;
    font-size: 8px;
    ;

  }

  .nosubmit.search.users {
    width: 52% !important;
    font-size: 10px !important;
  }

  .userinfo {
    grid-column: 2/5;
    display: block;
    text-align: left;
    font-size: 12px;
  }

  .page-title.user-title {
    font-size: 20px;
  }

  .hideTablett {
    display: block !important;
  }
}
</style>