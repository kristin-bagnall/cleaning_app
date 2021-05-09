import requests
import json

from datetime import date, timedelta

class InvoiceGenerator:
    """Generates Invoice object via invoice-generator API"""

    URL = "https://invoice-generator.com"
    logo = "https://res.cloudinary.com/jrcleaning/image/upload/v1620187377/sample.jpg"  # to do = figure out how logo image works. i think this needs to be a URL
    currency = "USD"
    payment_terms = "Due by payment due date"
    notes = "Thanks for being a loyal customer. We appreciate your business!"

    def __init__(self, 
                to, 
                sender = "J&R Crystal Cleaning",
                number=None, 
                date=date.today().isoformat(), 
                due_date=(date.today()+timedelta(days=30)).isoformat(), 
                amount_paid=0,
                items=[],
                item_name="Standard Clean",
                item_quantity=1,
                item_cost='150'
                ):
        self.to = to
        self.sender = sender
        self.number = number
        self.date = date
        self.due_date = due_date
        self.amount_paid = amount_paid
        self.items = [{}]
        self.items[0]['name'] = item_name
        self.items[0]['quantity'] = item_quantity
        self.items[0]['unit_cost'] = item_cost


    def _to_json(self):
        """
        Parsing the object as JSON string
        Please note we need also to replace the key sender to from, as per expected in the API but incompatible with from keyword inherent to Python
        """
        object_dict = self.__dict__
        object_dict['from'] = object_dict.get('sender')
        object_dict.pop('sender')

        return json.dumps(object_dict)


    def download(self, file_path):
        """ Directly send the request and store the file on path """
        json_string = self._to_json()
        response = requests.post(InvoiceGenerator.URL, json=json.loads(json_string), stream=True)
        if response.status_code == 200:
            open(file_path, 'wb').write(response.content)
        else:
            raise Exception(f"Invoice download request returned the following message:{response.json()} Response code = {response.status_code} ")