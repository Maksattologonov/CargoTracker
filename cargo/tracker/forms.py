from django import forms


class CargoForm(forms.Form):
    track_code = forms.CharField(label='Track Code', max_length=40, min_length=8)


class StatusForm(forms.Form):
    status = forms.CharField(label='Status', max_length=40, min_length=8)
    datetime = forms.CharField(label='Date/Time', max_length=40, min_length=8)
    location = forms.CharField(label='Location', max_length=40, min_length=8)


class ResultForm(forms.Form):
    trackingNumber = forms.CharField(label='Track Code', max_length=40, min_length=8)
    currentStatus = forms.CharField(label='Current Status', max_length=40, min_length=8)
    estimatedDeliveryDate = forms.CharField(label='Estimated Delivery Date', max_length=40, min_length=8)
    lastEvent = StatusForm()
