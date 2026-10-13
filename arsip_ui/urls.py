from django.urls import path

from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="default"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("login_history/", views.LoginHistoryView.as_view(), name="login_history"),
    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),
    path("dokumen/", views.DokumenView.as_view(), name="daftar_dokumen"),
    path("dokumen/<str:nama>", views.download_dokumen, name="download_dokumen"),
    path("dokumen/cari_dokumen/", views.CariDokumenView.as_view(), name="cari_dokumen"),
    path("dokumen/tambah_dokumen/", views.TambahDokumenView.as_view(), name="tambah_dokumen"),
    path("dokumen/ubah_dokumen/<str:pk>", views.UbahDokumenView.as_view(), name="ubah_dokumen")
]