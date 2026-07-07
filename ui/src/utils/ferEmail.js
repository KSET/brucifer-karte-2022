const DIACRITICS = { 'č': 'c', 'š': 's', 'ž': 'z', 'đ': 'd', 'ć': 'c' }
const normalize = (char) => DIACRITICS[char] || char

// FER JMBAG (003x): drop institution code + check digit → 5 digits.
// Transfer students keep their original JMBAG: drop only the check digit → 9 digits.
export function deriveFerEmail(name, surname, jmbag) {
    name = (name || '').trim()
    surname = (surname || '').trim()
    jmbag = (jmbag || '').trim()
    if (!name || !surname || !jmbag) return null

    const digits = jmbag.startsWith('003') ? jmbag.slice(4, 9) : jmbag.slice(0, 9)
    return `${normalize(name[0].toLowerCase())}${normalize(surname[0].toLowerCase())}${digits}@fer.hr`
}
