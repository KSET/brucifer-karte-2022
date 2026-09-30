import { reactive } from 'vue'
import { useToast } from 'primevue/usetoast'

export function useOptimisticList(store) {
  const toast = useToast()
  const savingCounts = reactive({})
  const saveSeq = {}

  function notifyError(detail) {
    toast.add({ severity: 'error', summary: 'Greška', detail, life: 3000 })
  }

  function isSaving(id) {
    return (savingCounts[id] || 0) > 0
  }

  async function savePatch(row, changes) {
    const current = store.state.list.find(x => x.id === row.id)
    if (!current) return

    const previous = {}
    const tickets = {}
    Object.keys(changes).forEach(k => {
      previous[k] = current[k]
      const key = `${row.id}:${k}`
      const ticket = (saveSeq[key] || 0) + 1
      saveSeq[key] = ticket
      tickets[k] = ticket
    })

    store.commit('PATCH_LIST_ITEM', { id: row.id, changes })
    savingCounts[row.id] = (savingCounts[row.id] || 0) + 1

    try {
      await store.dispatch('patch', { id: row.id, changes })
    } catch (e) {
      const revert = {}
      Object.keys(previous).forEach(k => {
        if (saveSeq[`${row.id}:${k}`] === tickets[k]) revert[k] = previous[k]
      })
      if (Object.keys(revert).length) {
        store.commit('PATCH_LIST_ITEM', { id: row.id, changes: revert })
      }
      notifyError('Promjena nije spremljena.')
    } finally {
      const next = (savingCounts[row.id] || 1) - 1
      if (next > 0) savingCounts[row.id] = next
      else delete savingCounts[row.id]
    }
  }

  async function reorder(rows) {
    try {
      await store.dispatch('reorder', rows)
    } catch (e) {
      notifyError(e?.stale
        ? 'Popis je u međuvremenu promijenjen; osvježen je, pokušaj ponovno.'
        : 'Redoslijed nije spremljen.')
    }
  }

  async function remove(row, confirmText) {
    if (!window.confirm(confirmText)) return

    try {
      await store.dispatch('remove', row.id)
    } catch (e) {
      notifyError('Brisanje nije uspjelo.')
    }
  }

  return { notifyError, isSaving, savePatch, reorder, remove }
}
