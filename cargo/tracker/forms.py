from django import forms


class CargoForm(forms.Form):
    track_code = forms.CharField(label='Track Code', max_length=40, min_length=8)


class CalculatorForm(forms.Form):
    """Simple calculator form for cargo dimensions and weight."""

    height = forms.FloatField(label='Height (cm)', min_value=0)
    width = forms.FloatField(label='Width (cm)', min_value=0)
    length = forms.FloatField(label='Length (cm)', min_value=0)
    weight = forms.FloatField(label='Weight (kg)', min_value=0)


class StatusForm(forms.Form):
    status = forms.CharField(label='Status', max_length=40, min_length=8)
    datetime = forms.CharField(label='Date/Time', max_length=40, min_length=8)
    location = forms.CharField(label='Location', max_length=40, min_length=8)


class ResultForm(forms.Form):
    trackingNumber = forms.CharField(label='Track Code', max_length=40, min_length=8)
    currentStatus = forms.CharField(label='Current Status', max_length=40, min_length=8)
    estimatedDeliveryDate = forms.CharField(label='Estimated Delivery Date', max_length=40, min_length=8)
    lastEvent = StatusForm()
