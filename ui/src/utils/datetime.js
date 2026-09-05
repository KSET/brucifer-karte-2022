const ZONE = 'Europe/Zagreb'

const partsFormatter = new Intl.DateTimeFormat('en-US', {
    timeZone: ZONE,
    year: 'numeric', month: '2-digit', day: '2-digit',
    hour: '2-digit', minute: '2-digit', second: '2-digit',
    hourCycle: 'h23',
})

const displayFormatter = new Intl.DateTimeFormat('hr-HR', {
    timeZone: ZONE,
    day: '2-digit', month: '2-digit', year: 'numeric',
    hour: '2-digit', minute: '2-digit',
    hourCycle: 'h23',
})

function zagrebParts(date) {
    const p = {}
    for (const { type, value } of partsFormatter.formatToParts(date)) p[type] = value
    return p
}

function zoneOffsetMinutes(date) {
    const p = zagrebParts(date)
    const asUTC = Date.UTC(+p.year, +p.month - 1, +p.day, +p.hour, +p.minute, +p.second)
    return (asUTC - Math.floor(date.getTime() / 1000) * 1000) / 60000
}

export function zagrebLocalToDate(localString) {
    if (!localString) return null
    const m = /^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2})/.exec(localString)
    if (!m) return null

    const [, y, mo, d, h, mi] = m.map(Number)
    if (y < 1970 || y > 9999) return null
    if (mo < 1 || mo > 12 || d < 1 || d > 31 || h > 23 || mi > 59) return null

    const guess = Date.UTC(y, mo - 1, d, h, mi)
    let instant = guess - zoneOffsetMinutes(new Date(guess)) * 60000
    instant = guess - zoneOffsetMinutes(new Date(instant)) * 60000
    const result = new Date(instant)

    const rt = zagrebParts(result)
    if (+rt.year !== y || +rt.month !== mo || +rt.day !== d) return null

    const drift = (+rt.hour * 60 + +rt.minute) - (h * 60 + mi)
    if (drift < 0 || drift > 60) return null
    return result
}

export function dateToZagrebLocalInput(date) {
    if (!date || Number.isNaN(date.getTime())) return ''
    const p = zagrebParts(date)
    return `${p.year}-${p.month}-${p.day}T${p.hour}:${p.minute}`
}

export function formatZagreb(date) {
    if (!date || Number.isNaN(date.getTime())) return ''
    const p = {}
    for (const { type, value } of displayFormatter.formatToParts(date)) p[type] = value
    return `${p.day}.${p.month}.${p.year}. ${p.hour}:${p.minute}`
}

export function parseStored(value) {
    if (!value || typeof value !== 'string') return null
    const d = new Date(value)
    return Number.isNaN(d.getTime()) ? null : d
}
