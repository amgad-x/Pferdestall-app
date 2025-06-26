from django.shortcuts import render, get_object_or_404, redirect
from django.forms import inlineformset_factory
from django.db.models import Q
from django.http import JsonResponse

from .models import Pferd, Fuetterung, ZugangHistorie
from .forms import PferdForm, ZugangForm, FuetterungFormSet


# 🔹 Startseite
def startseite(request):
    return render(request, 'stall/startseite.html')


# 🔹 Pferd hinzufügen (inkl. Fütterungen)
def pferd_hinzufuegen(request):
    if request.method == 'POST':
        form = PferdForm(request.POST, request.FILES)
        formset = FuetterungFormSet(request.POST, prefix='fuetterung_set')
        if form.is_valid() and formset.is_valid():
            pferd = form.save()
            fuetterungen = formset.save(commit=False)
            for f in fuetterungen:
                f.pferd = pferd
                f.save()
            return redirect('pferd_liste')
    else:
        form = PferdForm()
        formset = FuetterungFormSet(prefix='fuetterung_set')

    return render(request, 'stall/pferd_hinzufuegen.html', {
        'form': form,
        'formset': formset,
    })


# 🔹 Pferd Liste + Suche
def pferd_liste(request):
    query = request.GET.get('suche')
    if query:
        pferde = Pferd.objects.filter(Q(name__icontains=query) | Q(transponder_id__icontains=query))
    else:
        pferde = Pferd.objects.all()
    return render(request, 'stall/pferd_liste.html', {'pferde': pferde})


# 🔹 Pferd Details
def pferd_details(request, pk):
    pferd = get_object_or_404(Pferd, pk=pk)
    fuetterungen = Fuetterung.objects.filter(pferd=pferd).order_by('start_zeit')
    zutritte = ZugangHistorie.objects.filter(pferd=pferd).order_by('-zeitpunkt')[:4]

    return render(request, 'stall/pferd_details.html', {
        'pferd': pferd,
        'fuetterungen': fuetterungen,
        'zutritte': zutritte,
    })


# 🔹 Pferd bearbeiten (inkl. Intervall-Hinzufügen + Löschen)
def pferd_bearbeiten(request, pk):
    pferd = get_object_or_404(Pferd, pk=pk)

    FuetterungFormSetInline = inlineformset_factory(
        Pferd,
        Fuetterung,
        fields=('start_zeit', 'end_zeit'),
        extra=0,
        can_delete=True
    )

    if request.method == 'POST':
        form = PferdForm(request.POST, request.FILES, instance=pferd)
        formset = FuetterungFormSetInline(request.POST, instance=pferd, prefix='fuetterung_set')

        if form.is_valid() and formset.is_valid():
            form.save()

            # Speichern & Löschen richtig behandeln
            fuetterungen = formset.save(commit=False)

            for f in fuetterungen:
                f.pferd = pferd
                f.save()

            for obj in formset.deleted_objects:
                obj.delete()

            return redirect('pferd_liste')
    else:
        form = PferdForm(instance=pferd)
        formset = FuetterungFormSetInline(instance=pferd, prefix='fuetterung_set')

    return render(request, 'stall/pferd_bearbeiten.html', {
        'form': form,
        'formset': formset,
        'pferd': pferd,
    })


# 🔹 Pferd löschen
def pferd_loeschen(request, pk):
    pferd = get_object_or_404(Pferd, pk=pk)
    pferd.delete()
    return redirect('pferd_liste')


# 🔹 Zugangskontrolle mit Formular
def zugangskontrolle(request):
    if request.method == 'POST':
        form = ZugangForm(request.POST)
        if form.is_valid():
            pferd_id = form.cleaned_data['transponder_id']
            try:
                pferd = Pferd.objects.get(transponder_id=pferd_id)
                ZugangHistorie.objects.create(pferd=pferd)
                return render(request, 'stall/zugang_erlaubt.html', {'pferd': pferd})
            except Pferd.DoesNotExist:
                return render(request, 'stall/zugang_nicht_erlaubt.html')
    else:
        form = ZugangForm()
    return render(request, 'stall/zugangskontrolle.html', {'form': form})


# 🔹 JSON API für ESP32 o. Arduino
def zugang_api(request):
    pferd_id = request.GET.get("id")
    if not pferd_id:
        return JsonResponse({"status": "fehlt"})
    try:
        pferd = Pferd.objects.get(transponder_id=pferd_id)
        return JsonResponse({"status": "erlaubt", "name": pferd.name})
    except Pferd.DoesNotExist:
        return JsonResponse({"status": "verweigert"})
