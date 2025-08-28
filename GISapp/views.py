
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import Feeder, DT, LocationEntry, FeederDTSelection
from .forms import FeederForm

#from .models import Feeder, DT, FeederDTSelection



#def home(request):
#    return HttpResponse("Hello, this is my first Django app!")
#from django.shortcuts import render

def feeder_list(request):
    # Handle form submission
    if request.method == "POST":
        form = FeederForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('feeder_list')
    else:
        form = FeederForm()

    feeders = Feeder.objects.all()
    return render(request, 'GISapp/feeder_list.html', {'form': form, 'feeders': feeders})

def feeder_delete(request, pk):
    feeder = get_object_or_404(Feeder, pk=pk)
    feeder.delete()
    return redirect('feeder_list')


def home(request):
    return render(request, 'GISapp/home.html')

def dt_list(request):
    feeders = Feeder.objects.all()
    if request.method == "POST":
        dt_name = request.POST.get("dt_name")
        feeder_id = request.POST.get("feeder_id")
        capacity = request.POST.get("capacity")
        if dt_name and feeder_id and capacity:
            feeder = get_object_or_404(Feeder, id=feeder_id)
            DT.objects.create(name=dt_name, feeder=feeder, capacity=capacity)
        return redirect("dt_list")
    dts = DT.objects.select_related('feeder').all()  # so you can display capacity with dt name

    return render(request, "GISapp/dt_list.html", {"feeders": feeders, "dts": dts})
    #return render(request, "GISapp/dt_list.html", {"feeders": feeders})

def dt_delete(request, dt_id):
    dt = get_object_or_404(DT, id=dt_id)
    dt.delete()
    return redirect("dt_list")

def location_form(request):
    if request.method == "POST":
        name = request.POST.get("name")
        latitude = request.POST.get("latitude")
        longitude = request.POST.get("longitude")
        
        if name and latitude and longitude:
            LocationEntry.objects.create(
                name=name,
                latitude=latitude,
                longitude=longitude
            )
            return redirect('location_form')  # or redirect where you want
    
    return render(request, "GISapp/location_form.html")

# Create your views here.
def feeder_dt_select(request):
    # Variable stored in session to remember state 'N' or 'Y'
    var_value = request.session.get('var_value', 'N')

    feeders = Feeder.objects.all()

    selected_feeder_id = request.session.get('selected_feeder_id')
    selected_dt_id = request.session.get('selected_dt_id')

    # For the dropdown options based on the selected feeder (if any)
    dts = DT.objects.filter(feeder_id=selected_feeder_id) if selected_feeder_id else DT.objects.none()

    if request.method == "POST":
        if 'set_reset' in request.POST:
            # Handle SET/RESET button toggle
            if var_value == 'N':
                # Set var to Y and save selected feeder and dt in session
                feeder_id = request.POST.get('feeder')
                dt_id = request.POST.get('dt')

                if feeder_id and dt_id:
                    request.session['var_value'] = 'Y'
                    request.session['selected_feeder_id'] = feeder_id
                    request.session['selected_dt_id'] = dt_id
            else:
                # RESET: clear the saved values
                request.session['var_value'] = 'N'
                request.session['selected_feeder_id'] = None
                request.session['selected_dt_id'] = None

            return redirect('feeder_dt_select')

        elif 'submit_coords' in request.POST:
            # Handle form submission of StartPoint and EndPoint
            start_lat = request.POST.get('start_lat')
            start_lng = request.POST.get('start_lng')
            end_lat = request.POST.get('end_lat')
            end_lng = request.POST.get('end_lng')

            feeder_id = request.session.get('selected_feeder_id')
            dt_id = request.session.get('selected_dt_id')

            if feeder_id and dt_id and start_lat and start_lng and end_lat and end_lng:
                feeder = Feeder.objects.get(id=feeder_id)
                dt = DT.objects.get(id=dt_id)
                FeederDTSelection.objects.create(
                    feeder=feeder,
                    dt=dt,
                    start_point_lat=start_lat,
                    start_point_lng=start_lng,
                    end_point_lat=end_lat,
                    end_point_lng=end_lng
                )
                # After submit, reset start/end point inputs by clearing POST fields (handled in template)
            return redirect('feeder_dt_select')

    var_value = request.session.get('var_value', 'N')
    selected_feeder_id = request.session.get('selected_feeder_id')
    selected_dt_id = request.session.get('selected_dt_id')

    dts = DT.objects.filter(feeder_id=selected_feeder_id) if selected_feeder_id else DT.objects.none()

    context = {
        'feeders': feeders,
        'dts': dts,
        'var_value': var_value,
        'selected_feeder_id': int(selected_feeder_id) if selected_feeder_id else None,
        'selected_dt_id': int(selected_dt_id) if selected_dt_id else None,
    }
    return render(request, 'GISapp/feeder_dt_select.html', context)


# AJAX view to get DTs for a feeder (called on feeder dropdown change)
def ajax_get_dts(request):
    feeder_id = request.GET.get('feeder_id')
    dts = DT.objects.filter(feeder_id=feeder_id).values('id', 'name', 'capacity')
    dt_list = list(dts)
    return JsonResponse(dt_list, safe=False)

def show_feeder_dt_data(request):
    feeders = Feeder.objects.all()
    dts = None
    selected_feeder = request.GET.get('feeder')
    selected_dt = request.GET.get('dt')
    results = []

    if selected_feeder:
        dts = DT.objects.filter(feeder_id=selected_feeder)
    if selected_feeder and selected_dt and request.GET.get('show'):
        results = FeederDTSelection.objects.filter(feeder_id=selected_feeder, dt_id=selected_dt)

    context = {
        'feeders': feeders,
        'dts': dts,
        'selected_feeder': int(selected_feeder) if selected_feeder else None,
        'selected_dt': int(selected_dt) if selected_dt else None,
        'results': results,
    }
    return render(request, 'GISapp/show_feeder_dt.html', context)