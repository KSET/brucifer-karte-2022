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

        <div class="switchdiv">

          <h1 class="textfield" style="display: inline;">Vidljvo </h1>

          <label class="switch" @click="toggleVisibility">
            <input id="switch" type="checkbox" @input="changeVisible">
            <span class="slider round"></span>
          </label>
        </div>
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
  data() {
    return {
      isVisible: '',
    }
  },
  created() {
    axios.get(process.env.VUE_APP_BASE_URL + '/sponsors/?ordering=order',)
      .then(response => {
        if (response.data == 0) {
          this.visible = 0;
        } else {
          this.isVisible = response.data[response.data.length - 1].visible;
        }
        if (this.isVisible == '1') {
          document.getElementById("switch").checked = true;
        } else {
          document.getElementById("switch").checked = false;
        }

      })
  },
  methods: {
    changeVisible() {
      if (this.isVisible == 1) {
        var changenum = '0';
        this.isVisible = '0';
      } else {
        var changenum = '1';
        this.isVisible = '1';
      }
      axios.put(process.env.VUE_APP_BASE_URL + '/sponsors/314159/',
        { visible: changenum },
        { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } }
      )
        .then(() => {
        })
    },
    sleep(ms) {
      return new Promise(
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
          resp.data.splice(0, 1);

          resp.data.forEach(async element => {
            console.log("slanje maila")
            console.log(element)
            if (element.guestCap != 0) {

              await this.sleep(element.id*1000);

              console.log("mail poslan")

              let msg = element.name + " " + element.email + " " + element.slug

              let email = element.email

              const respp = await axios.post(process.env.VUE_APP_BASE_URL + '/mailer/0/send_mail/',
                {
                  subject: "[KSET] Link za uređivanje popisa za 40. Brucošijadu FER-a",
                  template: "sponsors_email",
                  message: msg,
                  name: element.name,
                  link: "https://brucosijada.kset.org/sponzori/" + element.slug,
                  to_mail: email
                },
                { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } }
              )
              const resppp = await axios.post(process.env.VUE_APP_BASE_URL + '/mailer/',
                {
                  subject: "[KSET] Link za uređivanje popisa za 40. Brucošijadu FER-a",
                  template: "sponsors_email",
                  message: msg,
                  name: element.name,
                  link: "https://brucosijada.kset.org/sponzori/" + element.slug,
                  to_mail: email
                },
                { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } }
              )
              console.log("mail poslan")

            }
          });
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