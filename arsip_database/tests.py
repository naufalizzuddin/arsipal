import io
import tempfile
from datetime import date
from pathlib import Path

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from PyPDF2 import PdfWriter
from PyPDF2.generic import DictionaryObject, NameObject, DecodedStreamObject

from .models import Arsip, LoginHistory


@override_settings(ALLOWED_HOSTS=['testserver'])
class ContainerStorageTests(TestCase):
    def setUp(self):
        self.media_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.media_directory.cleanup)
        static_root = Path(self.media_directory.name) / 'staticfiles'
        static_root.mkdir()
        self.media_settings = override_settings(
            MEDIA_ROOT=self.media_directory.name, STATIC_ROOT=static_root
        )
        self.media_settings.enable()
        self.addCleanup(self.media_settings.disable)
        self.user = get_user_model().objects.create_user(
            username='storage-test', password='test-password-only'
        )

    def test_anonymous_dashboard_redirects_to_login(self):
        response = self.client.get('/dashboard/')
        self.assertRedirects(response, '/login/')

    def test_login_opens_dashboard_and_records_history(self):
        response = self.client.post('/login/', {
            'username': 'storage-test', 'password': 'test-password-only'
        })
        self.assertRedirects(response, '/dashboard/')
        self.assertTrue(LoginHistory.objects.filter(user=self.user).exists())

    def test_pdf_metadata_and_download_use_configured_media_storage(self):
        # This directory differs from ./dokumen, as a mounted volume can do.
        writer = PdfWriter()
        writer.add_blank_page(width=300, height=300)
        page = writer.pages[0]
        page[NameObject('/Resources')] = DictionaryObject({
            NameObject('/Font'): DictionaryObject({
                NameObject('/F1'): DictionaryObject({
                    NameObject('/Type'): NameObject('/Font'),
                    NameObject('/Subtype'): NameObject('/Type1'),
                    NameObject('/BaseFont'): NameObject('/Helvetica'),
                })
            })
        })
        content = DecodedStreamObject()
        content.set_data(
            b'BT /F1 12 Tf 10 250 Td (Nomor : TEST/001) Tj '
            b'0 -20 Td (Perihal : Pengujian) Tj '
            b'0 -20 Td (Sifat : Biasa) Tj ET'
        )
        page[NameObject('/Contents')] = content
        pdf = io.BytesIO()
        writer.write(pdf)
        payload = pdf.getvalue()

        document = Arsip.objects.create(
            tanggal_surat=date(2026, 1, 1),
            file=SimpleUploadedFile('storage-test.pdf', payload, 'application/pdf'),
        )
        document.refresh_from_db()
        self.assertEqual(document.nomor, 'TEST/001')
        self.assertEqual(document.perihal, 'Pengujian')
        self.assertEqual(document.sifat, 'Biasa')
        self.assertTrue(document.file.storage.exists(document.file.name))

        self.client.force_login(self.user)
        response = self.client.get('/dokumen/' + document.file.name)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(b''.join(response.streaming_content), payload)
        response.close()
