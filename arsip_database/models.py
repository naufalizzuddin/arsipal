from django.db import models
from PyPDF2 import PdfReader
from django.core.validators import FileExtensionValidator
import re

from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

def cari_kata_penting(nama_file):
    nomor = r"Nomor\s*:\s*(.*)"
    perihal = r"Perihal\s*:\s*(.*)"
    hal = r"Hal\s*:\s*(.*)"
    sifat = r"Sifat\s*:\s*(.*)"
    surat = PdfReader(nama_file)
    page = surat.pages[0].extract_text()
    try:
        nomor = re.findall(nomor, page, re.MULTILINE)[0].split(" ")[0]
    except:
        nomor = ""
    try:
        perihal = re.findall(perihal, page, re.MULTILINE)[0].split(" ")[0]
    except:
        try:
            perihal = re.findall(hal, page, re.MULTILINE)[0].split(" ")[0]
        except:
            perihal = ""
    try:
        sifat = re.findall(sifat, page, re.MULTILINE)[0].split(" ")[0]
    except:
        sifat = ""
    kata_penting = {"nomor":nomor,"perihal":perihal,"sifat":sifat}
    return kata_penting

class Arsip(models.Model):
    tanggal_input = models.DateTimeField(auto_now_add=True)
    tanggal_surat = models.DateField()
    nomor = models.CharField(max_length=200, blank=True)
    sifat = models.CharField(max_length=200, blank=True)
    klasifikasi = models.CharField(max_length=200, blank=True)
    perihal = models.CharField(max_length=200, blank=True)
    file = models.FileField(validators=[FileExtensionValidator(allowed_extensions=["pdf"])])

    def save(self, *args, **kwargs):
            if("" in [self.nomor,self.sifat,self.perihal]):
                # Keep an uploaded stream open until FileField saves it to storage.
                self.file.open('rb')
                kata_penting = cari_kata_penting(self.file)
                self.file.seek(0)
                print(f"{kata_penting=}")
                if(self.nomor == ""):
                    self.nomor = kata_penting["nomor"]
                if(self.sifat == "" or self.sifat == "Tidak ada"):
                    if(kata_penting["sifat"].lower() in ["biasa", "rahasia", "penting", "segera", "amat rahasia", "khusus"]):
                        self.sifat = kata_penting["sifat"]
                if(self.perihal == ""):
                    self.perihal = kata_penting["perihal"]                            
            super().save(*args, **kwargs)

class LoginHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    login_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} logged in at {self.login_time}"
