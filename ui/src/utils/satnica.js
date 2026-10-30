import { zagrebLocalToDate, zagrebMinutes } from '@/utils/datetime'
import { stageLabel } from '@/utils/stages'

const EVENT_NIGHT = '2026-11-07'
const EVENT_NEXT_DAY = '2026-11-08'

export const EVENT_START = zagrebLocalToDate(`${EVENT_NIGHT}T20:00`)
export const EVENT_END = zagrebLocalToDate(`${EVENT_NEXT_DAY}T05:00`)

export const SATNICA_STAGES = [
    { key: 'menza', label: stageLabel('menza'), color: '#247C6BD9' },
    { key: 'kino', label: stageLabel('kino'), color: '#802F91D9' },
    { key: 'elektro', label: stageLabel('elektro'), color: '#D8B741D9' },
    { key: 'silent', label: 'Silent', color: '#166269D9' },
    { key: 'brucistar', label: 'Brucistar', color: '#5F1867D9' },
    { key: 'votafak', label: 'Votafak', color: '#24ACAFD9' },
]

// Times before 12:00 belong to the morning after the event night.
export function eventNightDate(hhmm) {
    const m = /^(\d{1,2}):(\d{2})$/.exec(hhmm || '')
    if (!m) return null
    const h = +m[1]
    const day = h < 12 ? EVENT_NEXT_DAY : EVENT_NIGHT
    return zagrebLocalToDate(`${day}T${String(h).padStart(2, '0')}:${m[2]}`)
}

export const HARDCODED_ACTS = [
    { name: 'Silent Disco', stage: 'silent', start: eventNightDate('21:00'), end: eventNightDate('05:00') },
    { name: 'Brucistar', stage: 'brucistar', start: eventNightDate('22:00'), end: eventNightDate('03:00') },
    { name: 'Votafak', stage: 'votafak', start: eventNightDate('23:59'), end: eventNightDate('03:59') },
]

export const pad = (n) => String(n).padStart(2, '0')

export function formatTime(date) {
    const m = zagrebMinutes(date)
    return `${pad(Math.floor(m / 60))}:${pad(m % 60)}`
}

export function actSlot(stageKey, start, end) {
    const stage = SATNICA_STAGES.find(s => s.key === stageKey)
    if (!stage) return null
    return {
        stage: stage.label,
        time: start && end ? `${formatTime(start)} – ${formatTime(end)}` : '',
        color: stage.color,
    }
}
