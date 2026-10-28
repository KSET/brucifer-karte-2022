export const STAGE_OPTIONS = [
    { value: 'menza', label: 'Menza' },
    { value: 'kino', label: 'Kino' },
    { value: 'elektro', label: 'Elektro' },
]

export function stageLabel(value) {
    return STAGE_OPTIONS.find(s => s.value === value)?.label || ''
}
