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
                        <InputText name="name" placeholder="Name" />
                        <Message v-if="$form.name?.invalid" severity="error" size="small" variant="simple">
                            {{ $form.name.error.message }}
                        </Message>
                    </div>

                    <!-- Surname -->
                    <div class="field">
                        <InputText name="surname" placeholder="Surname" />
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

                    <!-- Email -->
                    <div class="field">
                        <InputText name="email" type="email" placeholder="@fer.hr Email" />
                        <Message v-if="$form.email?.invalid" severity="error" size="small" variant="simple">
                            {{ $form.email.error.message }}
                        </Message>
                    </div>

                    <!-- GDPR -->
                    <div class="field">
                        <div style="display: flex; flex-direction: row; gap: 0.5rem; color: white;">
                            <Checkbox name="gdpr_accepted" binary inputId="gdpr_accepted" />
                            <label for="gdpr_accepted">
                                I agree to the processing of my personal data (
                                <a href="/Privola_za_prikupljanje_osobnih_podataka-Brucosijada_2025.pdf"
                                    target="_blank" rel="noopener noreferrer"
                                    style="color: #4da3ff; text-decoration: underline;">
                                    PRIVOLA ZA PRIKUPLJANJE OSOBNIH PODATAKA
                                </a>
                                )
                            </label>
                        </div>
                        <Message v-if="$form.gdpr_accepted?.invalid" severity="error" size="small" variant="simple">
                            {{ $form.gdpr_accepted.error.message }}
                        </Message>
                    </div>


                    <Button type="submit" label="Submit" />
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
import brucosiFormStore from '@/store/brucosiFormStore'

const normalize = (char) => {
    const map = { 'č': 'c', 'š': 's', 'ž': 'z', 'đ': 'd', 'ć': 'c' }
    return map[char] || char
}

function expectedFerEmail(values) {
    if (!values.name || !values.surname || !values.jmbag) {
        return null
    }
    let jmbagslice = values.jmbag

    if (jmbagslice.slice(0, 3) === '003') {
        jmbagslice = jmbagslice.slice(4, 9)
    } else if (jmbagslice.startsWith('0')) {
        jmbagslice = jmbagslice.slice(0, 9)
    } else {
        jmbagslice = jmbagslice.slice(2, 7)
    }

    const e_name = normalize(values.name[0].toLowerCase())
    const e_surname = normalize(values.surname[0].toLowerCase())

    return `${e_name}${e_surname}${jmbagslice}@fer.hr`
}

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
                email: '',
                jmbag: '',
                gdpr_accepted: false,
            },
            resolver: zodResolver(
                z.object({
                    name: z.string().min(1, { message: 'Name is required' }),
                    surname: z.string().min(1, { message: 'Surname is required' }),
                    jmbag: z.string().length(10, { message: 'JMBAG must be 10 digits' }),
                    email: z.string().email({ message: 'Valid email is required' }),
                    gdpr_accepted: z.literal(true, {
                        errorMap: () => ({ message: 'You must accept GDPR to continue' }),
                    }),
                }).superRefine((values, ctx) => {
                    const expected = expectedFerEmail(values)
                    if (values.email.toLowerCase() !== expected) {
                        ctx.addIssue({
                            code: 'custom',
                            path: ['email'],
                            message: 'Email must match your FER format (ip1234@fer.hr)',
                        })
                    }
                })
            ),
            toast: null,
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
                    summary: 'Invalid form',
                    detail: 'Please fill out all required fields correctly.',
                    life: 3000,
                })
                return
            }

            try {
                const res = await brucosiFormStore.dispatch('submit', values)

                this.toast.add({
                    severity: 'success',
                    summary: 'Submission received',
                    detail: 'Your data has been submitted successfully.',
                    life: 3000,
                })

                reset()
            } catch (e) {
                this.toast.add({
                    severity: 'info',
                    summary: 'Submission received',
                    detail: 'Your data has been submitted.',
                    life: 3000,
                })
            }
        },
    },
}
</script>


<style scoped>
.bw-page-container {}

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

    background-color: rgba(7, 72, 120, 0.7) !important;
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
