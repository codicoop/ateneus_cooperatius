
from django import forms
from PIL import Image
from io import BytesIO


class ExtendedImageField(forms.ImageField):
    def __init__(self, resize=None, filename=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resize = resize
        self.filename = filename

    def to_python(self, data):
        f = super().to_python(data)
        if not self.resize:
            return f

        byte_array = BytesIO()
        image = Image.open(f)
        # image.show()
        image = image.resize(self.resize)
        image.save(byte_array, format='PNG')
        f.name = self.filename if self.filename else f.name
        f.file = byte_array
        f.content_type = Image.MIME.get(image.format)
        f.image = image
        return f


