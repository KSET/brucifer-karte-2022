<template>
  <div class="sponsorsp">
    <Sidebar />
    <div class="admin-page-container">

      <div class="header">
        <h1 class="page-title">Sponzori</h1>
        <router-link class="icon7" to="/admin/sponsors-add/0">
          <img src="../../assets/icons/add-icon.svg">
        </router-link>

        <button class="button submit" style=" margin-top: 0px;  vertical-align: middle; " @click="sendMail">Pozovi
          sponzore</button>
      </div>

      <sponsors-table></sponsors-table>
    </div>
  </div>
</template>

<script>
import SponsorsTable from '@/components/AdminPanel/SponsorsTable.vue'
import Sidebar from '@/components/NavbarAndFooter/Sidebar.vue'

import axios from 'axios'
export default {
  name: 'SponsorsView',
  components: {
    SponsorsTable,
    Sidebar
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
                  subject: "[KSET] Link za uređivanje popisa za 41. Brucošijadu FER-a",
                  template: "sponsors_email",
                  message: msg,
                  name: element.name,
                  link: "https://brucosijada.kset.org/sponzori/" + element.slug,
                  to_mail: e
                })
              })
              await axios.post(process.env.VUE_APP_BASE_URL + '/mailer/',
                {
                  subject: "[KSET] Link za uređivanje popisa za 41. Brucošijadu FER-a",
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

<style >
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
  ;
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

/* Rounded sliders */
.slider.round {
  border-radius: 34px;
}

.slider.round:before {
  border-radius: 50%;
}
</style>