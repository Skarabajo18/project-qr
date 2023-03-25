from django.db import models
import uuid
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
import qrcode
from django.core.files.base import ContentFile
from django.urls import reverse
from io import BytesIO

# Create your models here.


class Tag (models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True,
                              upload_to="post", default="placeholder.png")
    state = models.BooleanField('Active', default=False)
    tags = models.ManyToManyField(Tag, blank=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    qr_code = models.ImageField(
        upload_to='qr_codes/',
        null=True,
        blank=True,
        editable=False
    )

    def save(self, *args, **kwargs):
        # Genera el código QR para el enlace del post
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(self.get_absolute_url_with_localhost())
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        # Almacena el código QR en el campo qr_code del modelo Post
        buffer = BytesIO()
        img.save(buffer)
        filename = f"{self.pk}.png"
        self.qr_code.save(filename, ContentFile(buffer.getvalue()), save=False)

        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', args=[str(self.id)])

    def get_absolute_url_with_localhost(self):
        return f'http://localhost:8000{self.get_absolute_url()}'
