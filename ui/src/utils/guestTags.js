// entry-desk requests give up after this so the event's flaky wifi can't leave the UI hanging
export const REQUEST_TIMEOUT = 10000;

export const BRUCOS_TAG = 'Brucoši';
// mirrors SPONSOR_TAG_MARKER in bruc/models.py: sponsor guests are tagged "<slug> VIP - Sponzor - <name>"
export const SPONSOR_TAG_MARKER = ' VIP - Sponzor - ';

export const isBrucos = (tag) => !!tag?.includes(BRUCOS_TAG);
export const isSponsor = (tag) => !!tag?.includes(SPONSOR_TAG_MARKER.trim());

export function displayTag(tag) {
  if (!tag) return '';
  const idx = tag.indexOf(SPONSOR_TAG_MARKER);
  return idx === -1 ? tag : tag.slice(idx + 1);
}
