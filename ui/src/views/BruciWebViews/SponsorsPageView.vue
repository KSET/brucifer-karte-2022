<template>
  <div class="bw-page-container sponsor-portal bw-overlay-footer bw-textured">
    <Toast :breakpoints="{ '550px': { width: 'calc(100vw - 32px)', right: '16px', left: '16px' } }" />

    <div class="sp-content">
      <div v-if="loading" class="sp-state">
        <p class="sp-text">Učitavanje…</p>
      </div>

      <div v-else-if="notFound" class="sp-state">
        <h1 class="bw-heading">Link nije valjan</h1>
        <p class="sp-text">Provjerite jeste li otvorili cijeli link iz maila ili se javite organizatoru.</p>
      </div>

      <div v-else class="sp-layout">
        <div class="sp-side bw-surface">
          <img v-if="sponsor.image && !logoFailed" class="sp-logo" :src="sponsor.image" :alt="sponsor.name"
            @error="logoFailed = true" />
          <h1 class="bw-heading">Popis uzvanika</h1>
          <p class="sp-text">{{ sponsor.name }}</p>

          <p class="sp-text sp-info">
            Uneseno: {{ guests.length }}{{ hasCap ? ` / ${sponsor.guestCap}` : '' }}<br>
            <template v-if="!isOpen">Unos je zatvoren. Ovo je vaš konačni popis.</template>
            <template v-else-if="deadlineText">Unos moguć do {{ deadlineText }}</template>
          </p>

          <form v-if="isOpen" class="sp-form" @submit.prevent="addGuest">
            <InputText v-model.trim="draft" placeholder="Ime i prezime" maxlength="100" autocomplete="off"
              aria-label="Ime i prezime" :disabled="capReached || busy" />
            <Button type="submit" class="sp-primary" label="Dodaj" :disabled="capReached || busy || !draft" />
          </form>
          <p v-if="isOpen && capReached" class="sp-text">Unijeli ste maksimalan broj gostiju.</p>
        </div>

        <div class="sp-list-panel">
          <h2 class="sp-list-title">Uneseni gosti</h2>
          <p v-if="!guests.length" class="sp-text sp-muted">Još nema unesenih gostiju.</p>

          <ul v-else class="sp-list">
            <li v-for="(guest, i) in guests" :key="guest.id" class="sp-row">
              <span class="sp-index">{{ i + 1 }}.</span>

              <template v-if="isOpen && editing && editing.id === guest.id">
                <InputText v-model.trim="editing.name" maxlength="100" :disabled="busy" autofocus
                  @keyup.enter="saveEdit" @keyup.esc="editing = null" />
                <div class="sp-actions">
                  <Button icon="pi pi-check" text rounded title="Spremi" aria-label="Spremi"
                    :disabled="busy || !editing.name" @click="saveEdit" />
                  <Button icon="pi pi-times" text rounded title="Odustani" aria-label="Odustani" :disabled="busy"
                    @click="editing = null" />
                </div>
              </template>

              <template v-else>
                <span class="sp-name">{{ guest.name }}</span>
                <span v-if="guest.entered" class="sp-text sp-muted">Ušao/la</span>
                <div v-else-if="isOpen" class="sp-actions">
                  <Button icon="pi pi-pencil" text rounded title="Uredi" aria-label="Uredi" :disabled="busy"
                    @click="startEdit(guest)" />
                  <Button icon="pi pi-trash" text rounded title="Obriši" aria-label="Obriši" :disabled="busy"
                    @click="removeGuest(guest)" />
                </div>
              </template>
            </li>
          </ul>
        </div>
      </div>
    </div>
    <Footer />
  </div>
</template>

<script>
import InputText from 'primevue/inputtext'
import Button from 'primevue/button'
import Toast from 'primevue/toast'
import { useToast } from 'primevue/usetoast'
import Footer from '@/components/NavbarAndFooter/Footer.vue'
import { publicApi } from '@/plugins/publicApi'
import { formatZagreb, parseStored } from '@/utils/datetime'

export default {
  name: 'SponsorsPage',
  components: { InputText, Button, Toast, Footer },

  setup() {
    return { toast: useToast() }
  },

  data() {
    return {
      loading: true,
      notFound: false,
      busy: false,
      sponsor: {},
      guests: [],
      draft: '',
      editing: null,
      logoFailed: false,
      now: Date.now(),
    }
  },

  computed: {
    base() {
      return `/sponsor-portal/${encodeURIComponent(this.$route.params.token)}/`
    },
    deadline() {
      return parseStored(this.sponsor.deadline)
    },
    deadlineText() {
      return formatZagreb(this.deadline)
    },
    isOpen() {
      // The server enforces the deadline too; re-checked here every 30s so the form closes on time.
      return this.sponsor.open && (!this.deadline || this.now <= this.deadline.getTime())
    },
    hasCap() {
      return !!this.sponsor.guestCap
    },
    capReached() {
      return this.hasCap && this.guests.length >= this.sponsor.guestCap
    },
  },

  async mounted() {
    this.clock = setInterval(() => { this.now = Date.now() }, 30000)
    try {
      await this.load()
    } catch (e) {
      if (e.response?.status === 404) this.notFound = true
      else this.notifyError(e)
    } finally {
      this.loading = false
    }
  },

  beforeUnmount() {
    clearInterval(this.clock)
  },

  methods: {
    async load() {
      const { data } = await publicApi.get(this.base)
      this.sponsor = data
      this.guests = data.guests
    },

    async run(fn) {
      if (this.busy) return
      this.busy = true
      try {
        await fn()
      } catch (e) {
        const status = e.response?.status
        this.notifyError(e)
        // 403/404/409 mean the list changed under us (deadline, a colleague on the same link, an admin): resync.
        if ([403, 404, 409].includes(status)) {
          this.editing = null
          try {
            await this.load()
          } catch {
            if (status === 403) this.sponsor = { ...this.sponsor, open: false }
          }
        }
      } finally {
        this.busy = false
      }
    },

    addGuest() {
      return this.run(async () => {
        const { data } = await publicApi.post(`${this.base}guests/`, { name: this.draft })
        this.guests.push(data)
        this.draft = ''
      })
    },

    startEdit(guest) {
      this.editing = { ...guest }
    },

    saveEdit() {
      if (!this.editing?.name) return
      const { id, name } = this.editing
      return this.run(async () => {
        const { data } = await publicApi.patch(`${this.base}guests/${id}/`, { name })
        this.guests.splice(this.guests.findIndex(g => g.id === id), 1, data)
        this.editing = null
      })
    },

    removeGuest(guest) {
      if (!window.confirm(`Obrisati gosta ${guest.name}?`)) return
      return this.run(async () => {
        await publicApi.delete(`${this.base}guests/${guest.id}/`)
        this.guests = this.guests.filter(g => g.id !== guest.id)
      })
    },

    notifyError(e) {
      const status = e.response?.status
      let detail = e.response?.data?.detail
      if (status === 400) detail = Object.values(e.response.data || {}).flat().join(' ')
      if (status === 429) detail = 'Previše zahtjeva, pokušajte ponovno za nekoliko minuta.'
      this.toast.add({ severity: 'error', summary: 'Greška', detail: detail || 'Pokušajte ponovno kasnije.', life: 5000 })
    },
  },
}
</script>

<style scoped>
.sponsor-portal {
  overflow: visible;
  justify-content: flex-start;
  background-image: none;
  background-color: var(--bw-teal-ink);
  min-height: 100vh;
  min-height: 100dvh;
}

/* No global border-box in this app; without it width: 100% + padding overflows on phones. */
.sp-layout,
.sp-side,
.sp-list-panel,
.sponsor-portal :deep(.p-inputtext) {
  box-sizing: border-box;
}

.sp-content {
  position: relative;
  z-index: 1;
  padding: 0 4vw calc(4vw + var(--bw-footer-measured-h, var(--bw-footer-total-h)));
  color: white;
}

.sp-state {
  max-width: 420px;
  margin: 0 auto;
  padding-top: clamp(96px, 14vw, 180px);
  text-align: center;
}

.sponsor-portal .sp-text {
  margin: 12px 0 0;
  padding: 0;
  font-family: 'Rubik', sans-serif;
  font-size: 16px;
  line-height: 1.5;
  color: white;
}

/* Two cards: sponsor info + add form | guest list */
.sp-layout {
  display: grid;
  grid-template-columns: minmax(0, 5fr) minmax(0, 7fr);
  gap: clamp(24px, 3vw, 48px);
  align-items: start;
  max-width: 68rem;
  margin: 0 auto;
  padding-top: clamp(56px, 8vw, 112px);
}

.sp-side {
  position: sticky;
  top: 24px;
  padding: clamp(24px, 2.5vw, 32px);
}

.sp-logo {
  display: block;
  max-width: 180px;
  max-height: 72px;
  margin-bottom: 24px;
  object-fit: contain;
}

.sponsor-portal .sp-info {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #FFFFFF1F;
}

.sp-form {
  display: flex;
  gap: 10px;
  margin-top: 24px;
}

.sponsor-portal :deep(.p-inputtext) {
  flex: 1;
  width: 100%;
  min-width: 0;
  padding: 0.65rem 0.8rem;
  font-family: 'Rubik', sans-serif;
  font-size: 16px;
  color: var(--bw-teal-ink);
  background: white;
  border: 2px solid transparent;
  border-radius: 8px;
  box-shadow: none;
}

.sponsor-portal :deep(.p-inputtext::placeholder) {
  color: #0C374380;
}

.sponsor-portal :deep(.p-inputtext:enabled:focus) {
  border-color: var(--bw-teal);
  box-shadow: none;
}

.sponsor-portal :deep(.p-inputtext:disabled) {
  opacity: 0.6;
}

.sp-list-panel :deep(.p-inputtext) {
  padding: 0.5rem 0.7rem;
  border-color: #0C374326;
}

.sp-list-panel :deep(.p-inputtext:enabled:focus) {
  border-color: var(--bw-teal-ink);
}

.sponsor-portal :deep(.sp-primary.p-button),
.sponsor-portal :deep(.sp-primary.p-button:not(:disabled):hover),
.sponsor-portal :deep(.sp-primary.p-button:not(:disabled):active) {
  flex: none;
  padding: 0.65rem 1.4rem;
  font-family: 'Rubik', sans-serif;
  font-weight: 500;
  color: var(--bw-teal-ink);
  background: var(--bw-teal);
  border: 0;
  border-radius: 8px;
}

.sponsor-portal :deep(.sp-primary.p-button:not(:disabled):hover) {
  background: #8DDADD;
}

.sponsor-portal :deep(.sp-primary.p-button:disabled) {
  opacity: 0.45;
}

/* Icon buttons. The global primary palette is all black, so Aura's hover would fill them black. */
.sponsor-portal :deep(.p-button-text),
.sponsor-portal :deep(.p-button-text:not(:disabled):hover),
.sponsor-portal :deep(.p-button-text:not(:disabled):active) {
  color: var(--bw-teal-ink);
  background: transparent;
  border-color: transparent;
}

.sponsor-portal :deep(.p-button-text:not(:disabled):hover) {
  background: #0C374314;
}

.sponsor-portal :deep(.p-button:focus-visible) {
  outline: 2px solid var(--bw-teal);
  outline-offset: 2px;
  box-shadow: none;
}

.sp-list-panel {
  min-height: 240px;
  padding: clamp(20px, 2.5vw, 32px);
  color: var(--bw-teal-ink);
  background: white;
  border-radius: 24px 0 0 0;
}

.sp-list-title {
  margin: 0;
  padding-bottom: 14px;
  font-family: 'Rubik', sans-serif;
  font-weight: 600;
  font-size: 20px;
  color: var(--bw-teal-ink);
  border-bottom: 2px solid #0C37431A;
}

.sponsor-portal .sp-list-panel .sp-text {
  margin-top: 16px;
  color: #0C374399;
}

.sp-list {
  list-style: none;
  margin: 0;
  padding: 0;
}

.sp-row {
  display: grid;
  grid-template-columns: 2rem minmax(0, 1fr) auto;
  align-items: center;
  gap: 8px;
  min-height: 3.25rem;
  border-bottom: 1px solid #0C374314;
}

.sp-row:last-child {
  border-bottom: none;
}

.sp-row:has(.p-inputtext) {
  padding: 6px 0;
}

.sp-index {
  font-family: 'Rubik', sans-serif;
  color: #0C374380;
}

.sp-name {
  font-family: 'Rubik', sans-serif;
  font-size: 16px;
  line-height: 1.35;
  overflow-wrap: anywhere;
}

.sp-actions {
  display: flex;
}

@media screen and (max-width: 980px) {
  .sp-layout {
    grid-template-columns: minmax(0, 1fr);
    max-width: 560px;
  }

  .sp-side {
    position: static;
  }

  .sp-list-panel {
    min-height: 0;
  }
}

@media screen and (max-width: 550px) {
  .sp-content {
    padding: 0 16px calc(8vw + var(--bw-footer-measured-h, var(--bw-footer-total-h)));
  }

  .sp-layout {
    gap: 20px;
    padding-top: 32px;
  }

  .sp-side,
  .sp-list-panel {
    padding: 20px 16px;
  }

  .sp-form {
    flex-direction: column;
  }
}
</style>
