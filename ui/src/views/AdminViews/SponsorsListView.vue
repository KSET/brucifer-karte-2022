<template>
  <div class="sponsorsp">
    <Sidebar />
    <div class="admin-page-container">

      <div class="header">
        <h1 class="page-title">Sponzori</h1>
        <router-link class="icon7" to="/admin/sponsors-add/0">
          <img src="../../assets/icons/add-icon.svg" />
        </router-link>

        <button class="button submit" style="margin-top: 0px; vertical-align: middle;" @click="sendMail">
          Pozovi sponzore
        </button>

        <ToggleSwitch v-model="isGrid" class="view-toggle" style="margin-left: 1rem;">
          <template #handle="{ checked }">
            <i :class="['pi', checked ? 'pi-th-large' : 'pi-list']" />
          </template>
        </ToggleSwitch>

      </div>

      <sponsors-table :view-mode="isGrid ? 'grid' : 'list'" />
    </div>
  </div>
</template>

<script>
import SponsorsTable from '@/components/AdminPanel/SponsorsTable.vue'
import Sidebar from '@/components/NavbarAndFooter/Sidebar.vue'
import ToggleSwitch from 'primevue/toggleswitch'

import axios from 'axios'
export default {
  name: 'SponsorsView',
  components: {
    SponsorsTable,
    Sidebar,
    ToggleSwitch
  },
  data() {
    return {
      isGrid: false
    }
  },
  methods: {
    async test() {
      console.log("1")

      await this.sleep(3000)
      console.log("1")
      await this.sleep(1000000)
      console.log("1")

      await this.sleep(1000000)
      console.log("1")
    },
    async sleep(ms) {
      return await new Promise(
        resolve => setTimeout(resolve, ms)
      );
    },

    async sendMail() {
      if (window.confirm("Klikom na OK šaljete mail SVIM sponzorima!!!")) {
        const resp = await axios.get(process.env.VUE_APP_BASE_URL + '/sponsors/')
        const res = await axios.get(process.env.VUE_APP_BASE_URL + '/mailer/')

        let emails = []
        resp.data.forEach(elementy => {
          if (elementy.email != '') {
            emails.push(elementy.email)
          }
        });

        let mailsent = 0;
        res.data.forEach(element => {
          emails.forEach(elementy => {
            if (element.message.includes(elementy)) {
              mailsent += 1;
              emails.pop(elementy)
            }
          });
        });

        if (mailsent > 0) {
          if (window.confirm(`Mail je već poslan ${mailsent}/${resp.data.length - 1} sponzora, klikom na 'OK' SVIM sponzorima će se ponovno poslati mail!!!`)) {
            mailsent = 0;
          }
        }
        if (mailsent == 0) {
          let emails = [];

          resp.data.forEach(async element => {
            if (element.guestCap != 0) {

              let msg = element.name + " " + element.email + " " + element.slug

              let email = element.email

              email = email.split(",")

              email.forEach((e) => {
                emails.push({
                  subject: "[KSET] Link za uređivanje popisa za 42. Brucošijadu FER-a",
                  template: "sponsors_email",
                  message: msg,
                  name: element.name,
                  link: "https://brucosijada.kset.org/sponzori/" + element.slug,
                  to_mail: e
                })
              })
              await axios.post(process.env.VUE_APP_BASE_URL + '/mailer/',
                {
                  subject: "[KSET] Link za uređivanje popisa za 42. Brucošijadu FER-a",
                  template: "sponsors_email",
                  message: msg,
                  name: element.name,
                  link: "https://brucosijada.kset.org/sponzori/" + element.slug,
                  to_mail: email.join(", ")
                },
                { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } }
              )
            }
          });

          await axios.post(process.env.VUE_APP_BASE_URL + '/mailer/send_mail/',
            {
              emails: emails
            },
            { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } }
          )

        }
      }

    }
  }
}

</script>

<style>
.header {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  position: relative;
}
</style>

<style>
.switchdiv {
  display: inline;
  margin-right: 2%;
  position: absolute;
  overflow: hidden;
  vertical-align: middle;
  right: 0%;
  top: 3%;


  margin-top: auto;
}

.switch {
  position: relative;
  vertical-align: middle;
  width: 60px;
  height: 34px;
}

.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #D9D9D9;
  -webkit-transition: .4s;
  transition: .4s;
}

.slider:before {
  position: absolute;
  content: "";
  height: 26px;
  width: 26px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  -webkit-transition: .4s;
  transition: .4s;
}

input:checked+.slider {
  background-color: black;
}

input:focus+.slider {
  box-shadow: 0 0 1px #2196F3;
}

input:checked+.slider:before {
  -webkit-transform: translateX(26px);
  -ms-transform: translateX(26px);
  transform: translateX(26px);
}

.slider.round {
  border-radius: 34px;
}

.slider.round:before {
  border-radius: 50%;
}

.view-toggle {
  --p-toggleswitch-width: 5rem;
  --p-toggleswitch-height: 2.5rem;
  --p-toggleswitch-handle-size: 2rem;

  --p-toggleswitch-background: #fff;
  --p-toggleswitch-checked-background: #000;

  --p-toggleswitch-handle-color: #fff;
  --p-toggleswitch-handle-background: #000;
  --p-toggleswitch-checked-handle-background: #fff;
  --p-toggleswitch-handle-checked-color: #000;
  --p-toggleswitch-handle-checked-background: #fff;

  --p-toggleswitch-border-color: #000;
  --p-toggleswitch-checked-border-color: #000;

  --p-toggleswitch-hover-background: var(--p-toggleswitch-background);
  --p-toggleswitch-checked-hover-background: var(--p-toggleswitch-checked-background);
  --p-toggleswitch-hover-border-color: var(--p-toggleswitch-border-color);
  --p-toggleswitch-checked-hover-border-color: var(--p-toggleswitch-checked-border-color);

  --p-toggleswitch-handle-checked-hover-color: var(--p-toggleswitch-handle-checked-color);
  --p-toggleswitch-handle-checked-hover-background: var(--p-toggleswitch-handle-checked-background);

  --p-toggleswitch-handle-hover-color: var(--p-toggleswitch-handle-color);
  --p-toggleswitch-handle-hover-background: var(--p-toggleswitch-handle-background);

}

.view-toggle .p-toggleswitch-handle {
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: none !important;
}

.view-toggle .p-toggleswitch-handle i {
  font-size: 1.2rem;
  line-height: 1;
  color: inherit;
}
</style>