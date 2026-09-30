<template>
  <div class="bw-page-container brucosi-page bw-overlay-footer bw-textured">
    <div class="bw-brucosi-content">

      <BwBackButton />

      <div class="bw-brucosi-head">
        <h2 class="bw-heading">Predregistracijska forma</h2>
        <p class="bw-brucosi-intro bw-text">Ispuni formu, predaj podatke te se zaputi na FER po svoju kartu po sniženoj cijeni!</p>
        <div class="bw-brucosi-note bw-surface bw-text">
          <img class="bw-brucosi-note-icon" src="@/assets/design-elements/brucosi.svg" alt="" aria-hidden="true" />
          <span>Isključivo za brucoše FER-a!</span>
        </div>
      </div>

      <div class="bw-panel">
        <Toast :breakpoints="{ '550px': { width: 'calc(100vw - 32px)', right: '16px', left: '16px' } }" />

        <Form v-slot="$form" :initialValues="initialValues" :resolver="resolver" @submit="onSubmit"
          class="bw-brucosi-form">
          <!-- Name -->
          <div class="field">
            <InputText class="bw-text" name="name" placeholder="Ime" />
            <Message v-if="$form.name?.invalid" severity="error" size="small" variant="simple">
              {{ $form.name.error.message }}
            </Message>
          </div>

          <!-- Surname -->
          <div class="field">
            <InputText class="bw-text" name="surname" placeholder="Prezime" />
            <Message v-if="$form.surname?.invalid" severity="error" size="small" variant="simple">
              {{ $form.surname.error.message }}
            </Message>
          </div>

          <!-- JMBAG -->
          <div class="field">
            <InputText class="bw-text" name="jmbag" placeholder="JMBAG" />
            <Message v-if="$form.jmbag?.invalid" severity="error" size="small" variant="simple">
              {{ $form.jmbag.error.message }}
            </Message>
          </div>

          <!-- GDPR -->
          <div class="field">
            <div class="gdpr-row">
              <Checkbox name="gdpr_accepted" binary inputId="gdpr_accepted" />
              <label for="gdpr_accepted" class="bw-text bw-text-light">
                Slažem se s
                <a href="/Privola_za_prikupljanje_osobnih_podataka-Brucosijada_2025.pdf" target="_blank"
                  rel="noopener noreferrer">Privolom za prikupljanje osobnih podataka</a>
              </label>
            </div>
            <Message v-if="$form.gdpr_accepted?.invalid" class="gdpr-message bw-text bw-text-light" severity="error" size="small" variant="simple">
              {{ $form.gdpr_accepted.error.message }}
            </Message>
          </div>

          <Button class="bw-text" type="submit" label="Pošalji" :loading="submitting" :disabled="submitting" />
        </Form>
      </div>

    </div>
    <Footer />
  </div>
</template>

<script>
import { Form } from '@primevue/forms'
import { zodResolver } from '@primevue/forms/resolvers/zod'
import { z } from 'zod'
import InputText from 'primevue/inputtext'
import Button from 'primevue/button'
import Message from 'primevue/message'
import Checkbox from 'primevue/checkbox'
import Toast from 'primevue/toast'
import { useToast } from 'primevue/usetoast'
import Footer from '@/components/NavbarAndFooter/Footer.vue'
import BwBackButton from '@/components/BruciWeb/BwBackButton.vue'
import { api } from '@/plugins/api'

export default {
  name: 'BrucosiView',

  components: {
    Form,
    InputText,
    Button,
    Message,
    Footer,
    BwBackButton,
    Checkbox,
    Toast,
  },

  setup() {
    return { toast: useToast() }
  },

  data() {
    return {
      initialValues: {
        name: '',
        surname: '',
        jmbag: '',
        gdpr_accepted: false,
      },
      resolver: zodResolver(
        z.object({
          name: z.string().min(1, { message: 'Ime je obavezno polje' }),
          surname: z.string().min(1, { message: 'Prezime je obavezno polje' }),
          jmbag: z.string().regex(/^\d{10}$/, { message: 'JMBAG mora biti 10 znamenki' }),
          gdpr_accepted: z.boolean().refine(val => val === true, { message: 'Prihvaćanje privole je obavezno', }),
        })
      ),
      submitting: false,
    }
  },

  methods: {
    async onSubmit({ values, valid, reset }) {
      if (!valid) {
        this.toast.add({
          severity: 'error',
          summary: 'Neispravan unos',
          detail: 'Molimo pregledajte podatke u formi te pokušajte ponovno.',
          life: 3000,
        })
        return
      }

      if (this.submitting) return
      this.submitting = true

      try {
        await api.post('/forms/', values)

        this.toast.add({
          severity: 'success',
          summary: 'Podaci spremljeni',
          detail: 'Vaši podaci su uspješno spremljeni.',
          life: 3000,
        })

        reset()
      } catch (e) {
        this.toast.add({ severity: 'error', life: 5000, ...this.submitErrorMessage(e) })
      } finally {
        this.submitting = false
      }
    },

    submitErrorMessage(e) {
      const status = e.response?.status

      if (status === 400) {
        const fieldErrors = Object.values(e.response.data || {}).flat().join(' ')
        return {
          summary: 'Neispravni podaci',
          detail: fieldErrors || 'Molimo pregledajte podatke u formi te pokušajte ponovno.',
        }
      }

      if (status === 429) {
        return {
          summary: 'Previše pokušaja',
          detail: 'Pokušaj ponovno za nekoliko minuta.',
        }
      }

      return {
        summary: 'Greška poslužitelja',
        detail: 'Podaci nisu spremljeni, pokušaj ponovno kasnije.',
      }
    },
  },
}
</script>

<style scoped>
.brucosi-page {
  overflow: visible;
  justify-content: flex-start;
  background-image: none;
  background-color: var(--bw-teal-ink);
  min-height: 100vh;
  min-height: 100dvh;
}

.bw-brucosi-content {
  position: relative;
  z-index: 1;
  padding: 0 4vw calc(4vw + var(--bw-footer-measured-h, var(--bw-footer-total-h)));
}

.bw-brucosi-head {
  text-align: center;
  color: white;
  padding-top: clamp(88px, 11vw, 132px);
}

.bw-brucosi-intro {
  max-width: 400px;
  margin: 0 auto;
  padding: clamp(24px, 3vw, 40px) 0 0;
}

.bw-brucosi-note {
  position: relative;
  display: inline-flex;
  align-items: center;
  margin-top: 40px;
  padding: 12px 24px 12px 80px;
}

.bw-brucosi-note-icon {
  position: absolute;
  left: 16px;
  top: 50%;
  width: 52px;
  height: 71px;
  transform: translateY(-50%);
  pointer-events: none;
}

.brucosi-page .bw-panel {
  width: 100%;
  max-width: 400px;
  padding: 24px;
  border-radius: 24px 0 0 0;
  color: var(--bw-teal-ink);
  background: linear-gradient(#0C37430D, #0C37430D), #FFFFFF;
}

.bw-brucosi-form {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.bw-brucosi-form .field {
  position: relative;
}

/* error sits inside the 24px gap so it doesn't shift the layout */
.bw-brucosi-form .field :deep(.p-message) {
  position: absolute;
  top: calc(100% + 2px);
  left: 0;
}

.gdpr-message :deep(.p-message-text) {
  font: inherit;
}

.bw-brucosi-form :deep(.p-inputtext) {
  width: 100%;
  padding: 0.6rem 0.75rem;
  color: var(--bw-teal-ink);
  background: #FFFFFF;
  border: 2px solid #0000001A;
  border-radius: 6px;
}

.bw-brucosi-form :deep(.p-inputtext::placeholder) {
  color: #0C374399;
}

.bw-brucosi-form :deep(.p-inputtext:enabled:focus) {
  border-color: var(--bw-teal-ink);
  box-shadow: none;
}

.gdpr-row {
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
}

.gdpr-row a {
  color: inherit;
  text-decoration: underline;
}

/* PrimeVue resets the border to 1px on hover/active, so every state sets it in full */
.bw-brucosi-form :deep(.p-button) {
  --overlay: transparent;
  --border: #FFFFFF1A;
}

.bw-brucosi-form :deep(.p-button:not(:disabled):hover) {
  --overlay: #FFFFFF1A;
}

.bw-brucosi-form :deep(.p-button:not(:disabled):active) {
  --overlay: #FFFFFF33;
  --border: #FFFFFF80;
}

.bw-brucosi-form :deep(.p-button),
.bw-brucosi-form :deep(.p-button:not(:disabled):hover),
.bw-brucosi-form :deep(.p-button:not(:disabled):active) {
  width: 100%;
  text-transform: uppercase;
  color: #FFFFFF;
  background: var(--bw-teal-ink);
  border: 2px solid var(--border);
  box-shadow: inset 0 0 0 100vmax var(--overlay);
}

@media screen and (max-width: 980px) {
  .bw-brucosi-content {
    padding: 0 6vw calc(6vw + var(--bw-footer-measured-h, var(--bw-footer-total-h)));
  }
}

@media screen and (max-width: 550px) {
  .bw-brucosi-content {
    padding: 0 6vw calc(8vw + var(--bw-footer-measured-h, var(--bw-footer-total-h)));
  }

  .brucosi-page .bw-panel {
    max-width: 100%;
  }
}
</style>
