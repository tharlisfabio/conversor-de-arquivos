from django.db import models

class ConvertedFile(models.Model):
    original_file = models.FileField(upload_to='uploads/')
    converted_file = models.FileField(upload_to='converted/')
    original_format = models.CharField(max_length=50)
    converted_format = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.original_file.name} -> {self.converted_format}"
