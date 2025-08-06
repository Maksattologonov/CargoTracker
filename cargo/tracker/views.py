from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from tracker.forms import CargoForm, CalculatorForm
from tracker.services import Ship24Service


# @login_required
def track(request):
    try:
        if request.method == 'POST':
            form = CargoForm(request.POST)
            if form.is_valid():
                ship = Ship24Service()
                parsed_data = ship.request(form.cleaned_data.get('track_code'))
                print(parsed_data)
                return render(request, "templates/tracker/tracking_data.html", {"trackings": parsed_data})
        else:
            form = CargoForm()
            return render(request, 'templates/tracker/tracker.html', {'form': form})
    except Exception as e:
        return render(request, 'templates/tracker/error.html', {'error': str(e)})


def home(request):
    return render(request, 'main.html')


def calculator(request):
    """Calculate shipment cost based on weight."""
    price = None
    if request.method == 'POST':
        form = CalculatorForm(request.POST)
        if form.is_valid():
            weight = form.cleaned_data['weight']
            price = weight * 3.2
    else:
        form = CalculatorForm()
    return render(
        request,
        'templates/tracker/calculator.html',
        {'form': form, 'price': price},
    )
