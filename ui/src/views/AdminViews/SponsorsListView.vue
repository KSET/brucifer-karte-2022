<template>
  <div class="sponsorsp">
    <Sidebar />
    <div class="admin-page-container sponsors-page">

      <div class="header sponsors-header">
        <h1 class="page-title">Sponzori</h1>
        <router-link class="add-link" to="/admin/sponsors-add/0" title="Dodaj sponzora">
          <img src="../../assets/icons/add-icon.svg">
        </router-link>

        <button class="button submit invite-button" @click="sendMail">Pozovi sponzore</button>
      </div>

      <sponsors-table></sponsors-table>
    </div>
  </div>
</template>

<script>
import SponsorsTable from '@/components/AdminPanel/SponsorsTable.vue'
import Sidebar from '@/components/NavbarAndFooter/Sidebar.vue'

import { api } from '@/plugins/api'
export default {
  name: 'SponsorsView',
  components: {
    SponsorsTable,
    Sidebar
  },
  methods: {
    async sendMail() {
      if (window.confirm("Klikom na OK šaljete mail SVIM sponzorima!!!")) {
        const resp = await api.get('/sponsors/')
        const res = await api.get('/mailer/')

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
            if (element.guestCap !== 0) {

              let msg = element.name + " " + element.email + " " + element.slug

              let email = element.email

              email = email.split(",")

              email.forEach((e) => {
                emails.push({
                  subject: "[KSET] Link za uređivanje popisa za 42. Brucošijadu FER-a",
                  template: "sponsors_email",
                  message: msg,
                  name: element.name,
                  slug: element.slug,
                  to_mail: e
                })
              })
              await api.post('/mailer/',
                {
                  subject: "[KSET] Link za uređivanje popisa za 42. Brucošijadu FER-a",
                  template: "sponsors_email",
                  message: msg,
                  name: element.name,
                  slug: element.slug,
                  to_mail: email.join(", ")
                }
              )
            }
          });

          await api.post('/mailer/send_mail/', { emails: emails })

        }
      }

    }
  }
}

</script>

<style scoped>
.sponsors-page {
  display: flex;
  flex-direction: column;
  height: 93vh;
  min-height: 0;
  box-sizing: border-box;
  margin-left: 25%;
  margin-right: 0;
  padding-left: 1rem;
  padding-right: 1rem;
}

@media screen and (max-width: 900px) {
  .sponsors-page {
    margin-left: 0;
  }
}

.sponsors-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}

.sponsors-header .page-title {
  margin: 0;
}

.add-link {
  display: inline-flex;
  align-items: center;
}

.add-link img {
  width: 2rem;
  height: 2rem;
  display: block;
}

.invite-button {
  margin-top: 0;
  margin-left: auto;
}
</style>
