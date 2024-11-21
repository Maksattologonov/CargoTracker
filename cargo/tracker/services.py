import json

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
import requests


class Ship24Service:
    url = 'https://api.ship24.com/public/v1/trackers/track'
    token = settings.BASE_SHIP24_TOKEN
    data = ''
    results = {}

    def request(self, track_code):
        response = requests.post(url=self.url,
                                 data=json.dumps({"trackingNumber": f'{track_code}'}),
                                 headers={'Content-Type': 'application/json',
                                          'Authorization': f'Bearer {self.token}'})
        self.data = response.json()

        if "errors" in self.data and self.data["errors"]:
            error_message = self.data["errors"][0]["message"]
            raise ObjectDoesNotExist(error_message)

        self.results = {}
        trackings = self.data.get("data", {}).get("trackings", [])

        for tracking in trackings:
            tracking_number = tracking.get("tracker", {}).get("trackingNumber")
            current_status = tracking.get("shipment", {}).get("statusMilestone")
            estimated_delivery_date = tracking.get("shipment", {}).get("delivery", {}).get("estimatedDeliveryDate")

            last_event = max(tracking.get("events", []), key=lambda e: e.get("datetime", ""), default={})
            last_status = last_event.get("status")
            last_datetime = last_event.get("datetime")
            last_location = last_event.get("location")

            self.results.update({
                "trackingNumber": tracking_number,
                "currentStatus": current_status,
                "estimatedDeliveryDate": estimated_delivery_date,
                "lastEvent": {
                    "status": last_status,
                    "datetime": last_datetime,
                    "location": last_location
                }
            })
        return self.results
