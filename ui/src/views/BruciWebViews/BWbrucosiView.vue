<template>
    <div class="bw-page-container">
        <div style="padding: 0 1rem;">
            <div class="text-block">
                <h1>Predregistracijska forma za brucoške karte*</h1>
                <p>Ispuni formu, predaj podatke te se zaputi na FER po svoju kartu po sniženoj cijeni!</p>
                <p>*isključivo za brucoše FER-a</p>
            </div>

            <div class="submission-form">
                <Toast />

                <Form v-slot="$form" :initialValues="initialValues" :resolver="resolver" @submit="onSubmit"
                    class="flex flex-col gap-4 w-full sm:w-96">
                    <!-- Name -->
                    <div class="field">
                        <InputText name="name" placeholder="Ime" />
                        <Message v-if="$form.name?.invalid" severity="error" size="small" variant="simple">
                            {{ $form.name.error.message }}
                        </Message>
                    </div>

                    <!-- Surname -->
                    <div class="field">
                        <InputText name="surname" placeholder="Prezime" />
                        <Message v-if="$form.surname?.invalid" severity="error" size="small" variant="simple">
                            {{ $form.surname.error.message }}
                        </Message>
                    </div>

                    <!-- JMBAG -->
                    <div class="field">
                        <InputText name="jmbag" placeholder="JMBAG" />
                        <Message v-if="$form.jmbag?.invalid" severity="error" size="small" variant="simple">
                            {{ $form.jmbag.error.message }}
                        </Message>
                    </div>

                    <!-- GDPR -->
                    <div class="field">
                        <div style="display: flex; flex-direction: row; gap: 0.5rem; color: white;">
                            <Checkbox name="gdpr_accepted" binary inputId="gdpr_accepted" />
                            <label for="gdpr_accepted">
                                Slažem se s
                                <a href="/Privola_za_prikupljanje_osobnih_podataka-Brucosijada_2025.pdf" target="_blank"
                                    rel="noopener noreferrer" style="color: #4da3ff; text-decoration: underline;">
                                    Privolom za prikupljanje osobnih osobnih podataka </a>

                            </label>
                        </div>
                        <Message v-if="$form.gdpr_accepted?.invalid" severity="error" size="small" variant="simple">
                            {{ $form.gdpr_accepted.error.message }}
                        </Message>
                    </div>


                    <Button type="submit" label="Submit" :loading="submitting" :disabled="submitting" />
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
import { api } from '@/plugins/api'

export default {
    name: 'JmbagForm',

    components: {
        Form,
        InputText,
        Button,
        Message,
        Footer,
        Checkbox,
        Toast,
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
            toast: null,
            submitting: false,
        }
    },

    mounted() {
        this.toast = useToast()
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
                await api.post('/forms/brucosi-form-submit/', values)

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
.text-block {
    text-align: center;
    margin: 2rem auto 0 auto;
    max-width: 40rem;
}

.submission-form {
    padding: 1.5rem;
    max-width: 30rem;
    margin: 2rem auto 3rem auto;
    width: 100%;

    background-color: var(--bw-dialog-bg) !important;
    border: 1px solid white;
    border-radius: 12px;
}

input,
button {
    width: 100%;
}

p {
    margin: 0;
}

.submission-form .field {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
    margin-bottom: 1rem;

    min-height: 4.5rem;
}

.submission-form input {
    width: 100%;
    padding: 0.6rem 0.75rem;
    border-radius: 6px;
    border: 1px solid #ccc;
}

.submission-form .p-message {
    min-height: 1.25rem;
}
</style>
