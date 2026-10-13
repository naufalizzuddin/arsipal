from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, FileResponse, HttpResponseNotFound

from django.template import loader
from arsip_database.models import Arsip, LoginHistory

from django.views import generic

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin

from django.db.models import Count
from django.db.models.functions import ExtractYear, ExtractMonth

from django.urls import reverse_lazy
from .forms import TambahDokumenForm

from django.utils import timezone
from datetime import datetime, timedelta



class IndexView(generic.RedirectView):
    url = "dashboard"

class DokumenView(LoginRequiredMixin, generic.ListView):
    template_name = "arsip_ui/index.html"
    context_object_name = "arsip_terbaru"

    def get_queryset(self):
        return Arsip.objects.order_by("-tanggal_input")

class DashboardView(LoginRequiredMixin, generic.ListView):
    template_name = "arsip_ui/dashboard.html"
    context_object_name = "arsip_data"

    print(timezone.now())
    def get_queryset(self):
        jumlah_dokumen = len(Arsip.objects.all())
        jumlah_hari_ini = len(Arsip.objects.filter(tanggal_input__date=timezone.now().date()))
        jumlah_biasa = len(Arsip.objects.filter(sifat__icontains="biasa"))
        jumlah_segera = len(Arsip.objects.filter(sifat__icontains="segera"))
        jumlah_penting = len(Arsip.objects.filter(sifat__icontains="penting"))
        jumlah_rahasia = len(Arsip.objects.filter(sifat__icontains="rahasia"))
        jumlah_amat_rahasia = len(Arsip.objects.filter(sifat__icontains="amat rahasia"))
        jumlah_khusus = len(Arsip.objects.filter(sifat__icontains="khusus"))
        arsip_per_bulan = (
            Arsip.objects
                .annotate(year=ExtractYear('tanggal_surat'), month=ExtractMonth('tanggal_surat'))
                .values('year', 'month')
                .annotate(count=Count('id'))
                .order_by('year', 'month')
        )   

        arsip_dict = {}
        for arsip in arsip_per_bulan:
            year = arsip['year']
            month = arsip['month']
            count = arsip['count']
            
            if year not in arsip_dict:
                arsip_dict[year] = [0] * 12
            
            arsip_dict[year][month - 1] = count
            
        arsip_by_year = arsip_dict.keys()

        context = {
        "jumlah_dokumen":jumlah_dokumen,
        "jumlah_hari_ini": jumlah_hari_ini,
        "jumlah_penting":jumlah_penting,
        "jumlah_biasa":jumlah_biasa,
        "jumlah_segera":jumlah_segera,
        "jumlah_rahasia":jumlah_rahasia,
        "jumlah_amat_rahasia":jumlah_amat_rahasia,
        "jumlah_khusus":jumlah_khusus,
        "tahun_arsip":arsip_by_year,
        "arsip_dict":arsip_dict
        }
        return context

class CariDokumenView(LoginRequiredMixin, generic.ListView):
    template_name = "arsip_ui/index.html"
    context_object_name = "arsip_terbaru"

    def get_queryset(self):
        if(self.request.GET["Kategori"][0] != ''):
            if(self.request.GET["Kategori"] == 'Tanggal Input'):
                tanggal_input = self.request.GET["nama_dicari"]
                start_date = ""
                end_date = ""
                start_date = datetime.combine(timezone.datetime.strptime(tanggal_input, '%Y-%m-%d').date(), datetime.min.time())
                if("date_until" in self.request.GET):
                    tanggal_input_hingga = self.request.GET["date_until"]
                    if(self.request.GET["date_until"] != ""):
                        end_date = datetime.combine(timezone.datetime.strptime(tanggal_input_hingga, '%Y-%m-%d').date(), datetime.min.time())
                    else:
                        end_date = start_date + timedelta(days=1)
                arsip_terbaru = Arsip.objects.filter(tanggal_input__gte=start_date ,tanggal_input__lt=end_date)

            if(self.request.GET["Kategori"] == 'Tanggal Surat'):
                tanggal_surat = self.request.GET["nama_dicari"]
                start_date = ""
                end_date = ""
                start_date = datetime.combine(timezone.datetime.strptime(tanggal_surat, '%Y-%m-%d').date(), datetime.min.time())
                if("date_until" in self.request.GET):
                    tanggal_surat_hingga = self.request.GET["date_until"]
                    if(self.request.GET["date_until"] != ""):
                        end_date = datetime.combine(timezone.datetime.strptime(tanggal_surat_hingga, '%Y-%m-%d').date(), datetime.min.time())
                    else:
                        end_date = start_date + timedelta(days=1)
                arsip_terbaru = Arsip.objects.filter(tanggal_surat__gte=start_date ,tanggal_surat__lt=end_date)


            if(self.request.GET["Kategori"] == 'Nomor'):
                nomor = self.request.GET["nama_dicari"]
                arsip_terbaru = Arsip.objects.filter(nomor__icontains=nomor) 

            if(self.request.GET["Kategori"] == 'Perihal'):
                perihal = self.request.GET["nama_dicari"]
                arsip_terbaru = Arsip.objects.filter(perihal__icontains=perihal)  

            if(self.request.GET["Kategori"] == 'Sifat'):
                sifat = self.request.GET["nama_dicari"]
                arsip_terbaru = Arsip.objects.filter(sifat__icontains=sifat) 

            if(self.request.GET["Kategori"] == 'Klasifikasi'):
                klasifikasi = self.request.GET["nama_dicari"]
                arsip_terbaru = Arsip.objects.filter(sifat__icontains=klasifikasi) 

            return arsip_terbaru
        
class UbahDokumenView(LoginRequiredMixin, generic.FormView):
    template_name = "arsip_ui/ubah_dokumen.html"
    form_class = TambahDokumenForm
    success_url = reverse_lazy("daftar_dokumen")

    def get_initial(self):
        pk = self.kwargs.get('pk')
        doc = get_object_or_404(Arsip, id=pk)
        data_dokumen = {
            "tanggal_surat":doc.tanggal_surat,
            "nomor":doc.nomor,
            "sifat":doc.sifat,
            "klasifikasi":doc.klasifikasi,
            "perihal":doc.perihal,
            "file":doc.file.name
        }
        return data_dokumen

    def form_valid(self, form):
        print(form.cleaned_data)
        action = self.request.POST.get('action')
        if(action == "save"):
            doc = get_object_or_404(Arsip, id=self.kwargs.get('pk'))
            form = TambahDokumenForm(self.request.POST, self.request.FILES, instance=doc) 
            if form.is_valid():
                form.save()
        elif(action == "delete"):
            doc = get_object_or_404(Arsip, id = self.kwargs.get('pk'))
            doc.file.delete(save=False)
            doc.delete()
        return super().form_valid(form)

    def form_invalid(self, form):
        print("Input Form Error")
        for field, errors in form.errors.items():
            for error in errors:
                print(f"{field}: {error}")
        return super().form_invalid(form) 

class TambahDokumenView(LoginRequiredMixin, generic.FormView):
    template_name = "arsip_ui/tambah_dokumen.html"
    form_class = TambahDokumenForm
    success_url = reverse_lazy("daftar_dokumen")

    def form_valid(self, form):
        print(form.cleaned_data)
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        print("Input Form Error")
        for field, errors in form.errors.items():
            for error in errors:
                print(f"{field}: {error}")
        return super().form_invalid(form) 

class LoginView(generic.FormView):
    template_name = "arsip_ui/login.html"
    form_class = AuthenticationForm
    success_url = reverse_lazy("dashboard")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)        

    def form_valid(self, form):
        print(form.cleaned_data)
        print(self.request.POST)
        user = authenticate(self.request, username=form.cleaned_data["username"],  password=form.cleaned_data["password"])
        if user is not None:
            login(self.request, user)
            messages.success(self.request, f'Login berhasil! \n Selamat datang, {user}.')
            if(self.request.POST.get("remember_me")):
                self.request.session.set_expiry(24 * 3600 * 30)
            else:
                self.request.session.set_expiry(0)
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        print("Input Form Error")
        for field, errors in form.errors.items():
            for error in errors:
                print(f"{field}: {error}")
        messages.error(self.request, "Login gagal! \n Periksa kembali username atau password Anda.")
        return super().form_invalid(form)    
    
class LoginHistoryView(LoginRequiredMixin, generic.ListView):
    template_name = "arsip_ui/login_history.html"
    context_object_name = "logins"

    def get_queryset(self):
        return LoginHistory.objects.order_by("-login_time")
    

def logout_view(request):
    logout(request)
    messages.info(request, "Anda telah logout.")
    return redirect("login")

def download_dokumen(request, nama):
    try:
        response = FileResponse(open(f"dokumen/{nama}", "rb"))
        return response
    except:
        return HttpResponseNotFound("404 : dokumen tidak ditemukan")

