from django import forms
from arsip_database.models import Arsip

class TambahDokumenForm(forms.ModelForm):
    class Meta:
        model = Arsip
        fields = ["tanggal_surat", "nomor", "sifat", "klasifikasi", "perihal", "file"]