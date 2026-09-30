import os
from io import BytesIO

from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from PIL import Image, ImageOps, UnidentifiedImageError

MAX_SIZE = 2000
QUALITY = 80


def to_webp(field_file, max_size=MAX_SIZE, quality=QUALITY):
    '''Return a resized WebP ContentFile, or None if the file is already a small enough WebP.'''
    try:
        field_file.seek(0)
        img = Image.open(field_file)
        img.load()
    except (UnidentifiedImageError, OSError) as e:
        raise ValidationError(f'Invalid image file: {e}')

    if img.format == 'WEBP' and max(img.size) <= max_size:
        return None

    img = ImageOps.exif_transpose(img)
    has_alpha = img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info)
    img = img.convert('RGBA' if has_alpha else 'RGB')
    img.thumbnail((max_size, max_size), Image.LANCZOS)

    buf = BytesIO()
    img.save(buf, format='WEBP', quality=quality, method=6)

    stem = os.path.splitext(os.path.basename(field_file.name))[0]
    return ContentFile(buf.getvalue(), name=f'{stem}.webp')
