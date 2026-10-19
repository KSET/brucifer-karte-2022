import visibilityStore from '@/store/visibilityStore'


export function enabledGuestsValue(name) {
  if (!visibilityStore.getters.sponsorsInputClosed) return 1
  return window.confirm(`Rok za unos je istekao. Ponovno otvoriti popis za "${name}" i nakon roka?`) ? 2 : 1
}
