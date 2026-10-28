"""Diacritic-insensitive guest search: 'cosic', 'Ćosić' and 'ĆOSIĆ' all match each other."""
import unicodedata

from django.db.models import Case, IntegerField, Q, Value, When

# A value matches if either spelling matches:
#   short: đ -> d and dj -> d, so 'duro', 'djuro' and 'Đuro' are all equal
#   long:  đ -> dj, so 'jur' still finds 'Djurdjević' and everything a plain search finds
SHORT, LONG = 'short', 'long'


def fold(value, variant=SHORT):
    if value is None:
        return None
    # NFKD splits 'č' into 'c' + caron, also when the text arrived already decomposed (pasted from macOS),
    # so dropping the marks covers every accent ('Zoë', 'Müller'); đ doesn't decompose and is mapped by hand,
    # together with its lookalike ð; invisible format characters (zero-width space, soft hyphen) that come
    # along with names pasted from chats and spreadsheets are dropped too
    value = unicodedata.normalize('NFKD', str(value).lower())
    value = ''.join(c for c in value if not unicodedata.combining(c) and unicodedata.category(c) != 'Cf')
    value = value.replace('ð', 'đ').replace('đ', 'd' if variant == SHORT else 'dj')
    return value.replace('dj', 'd') if variant == SHORT else value


def search_key(name, surname):
    """Stored on Guests.searchKey. Every word starts after a space, so ' ' + term is a prefix match,
    and the surname comes first, so ordering by the key sorts by surname, then name.
    Sponsor and imported guests often have the whole name in one field, so empty fields and extra spaces
    are dropped; a leftover space would sort before every letter.
    The two spellings are joined by a newline, which no search term can contain, so no term matches across them.
    Changing fold() or this key needs a data migration that rebuilds every key, like 0092 does."""
    full_name = f"{surname or ''} {name or ''}"
    return '\n'.join(' ' + ' '.join(fold(full_name, variant).split()) for variant in (SHORT, LONG))


def _variants(term):
    # a set, because most terms have no đ/dj and both spellings are the same
    return {fold(term, SHORT), fold(term, LONG)}


def name_search_q(terms):
    """Every term has to appear in the name or surname."""
    q = Q()
    for term in terms:
        term_q = Q()
        for variant in _variants(term):
            term_q |= Q(searchKey__contains=variant)
        q &= term_q
    return q


def name_rank(terms):
    """How many terms a name or surname starts with."""
    rank = Value(0)
    for term in terms:
        starts = Q()
        for variant in _variants(term):
            starts |= Q(searchKey__contains=f' {variant}')
        rank += Case(When(starts, then=Value(1)), default=Value(0))
    rank.output_field = IntegerField()
    return rank
