const DIACRITICS = { 'č': 'c', 'š': 's', 'ž': 'z', 'đ': 'd', 'ć': 'c' }
const normalize = (char) => DIACRITICS[char] || char

export function deriveFerEmail(name, surname, jmbag) {
    name = (name || '').trim()
    surname = (surname || '').trim()
    jmbag = (jmbag || '').trim()
    if (!name || !surname || !jmbag) return null

    const digits = jmbag.startsWith('003') ? jmbag.slice(4, 9) : jmbag.slice(0, 9)
    const initials = normalize(name[0].toLowerCase()) + normalize(surname[0].toLowerCase())
    if (!/^[a-z]{2}$/.test(initials) || !/^[0-9]{5}([0-9]{4})?$/.test(digits)) return null
    return `${initials}${digits}@fer.hr`
}
