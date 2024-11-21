from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from tracker.forms import CargoForm
from tracker.services import Ship24Service


# @login_required
def track(request):
    try:
        if request.method == 'POST':
            form = CargoForm(request.POST)
            if form.is_valid():
                ship = Ship24Service()
                parsed_data = ship.request(form.cleaned_data.get('track_code'))
                return render(request, "tracker/tracking_data.html", {"trackings": parsed_data})
        else:
            form = CargoForm()
        return render(request, 'tracker/tracker.html', {'form': form})
    except Exception as e:
        return render(request, 'tracker/error.html')
