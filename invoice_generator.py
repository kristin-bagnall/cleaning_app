import requests
import json

from datetime import datetime

class InvoiceGenerator:
  """Generates Invoice object via invoice-generator API"""

  URL = "https://invoice-generator.com"
  logo = "/static/images/logo.png"  # to do = figure out how logo image works
  currency = "USD"
  payment_terms = "Due by payment due date"
  notes = "Thanks for being a loyal customer. We appreciate your business!"

  def __init__(self, 
              to, 
              sender = "J&R Crystal Cleaning",
              number=None, 
              date=datetime.now().strftime("%d-%b-%Y") , 
              due_date=datetime.now().strftime("%d-%b-%Y"), #need to figure out how to add 30 days to today
              amount_paid=0, 
              ):
    self.to = to
    self.sender = sender
    self.number = number
    self.date = date
    self.due_date = due_date
    self.amount_paid = amount_paid
    self.items = []

  def _to_json(self):
      """
      Parsing the object as JSON string
      Please note we need also to replace the key sender to from, as per expected in the API but incompatible with from keyword inherent to Python
      We are also resetting the two list of Objects items and custom_fields so that it can be JSON serializable
      """
      object_dict = self.__dict__
      object_dict['from'] = object_dict.get('sender')
      object_dict.pop('sender')

      for index, item in enumerate(object_dict['items']):
          object_dict['items'][index] = item.__dict__
      return json.dumps(object_dict)

  def add_item(self, name=None, quantity=0, unit_cost=0.0, description=None):
      """ Add item to the invoice """
      self.items.append(Item(
          name=name,
          quantity=quantity,
          unit_cost=unit_cost,
          description=description
      ))

  def download(self, file_path):
      """ Directly send the request and store the file on path """
      json_string = self._to_json()
      response = requests.post(InvoiceGenerator.URL, json=json.loads(json_string), stream=True)
      if response.status_code == 200:
          open(file_path, 'wb').write(response.content)
      else:
          raise Exception(f"Invoice download request returned the following message:{response.json()} Response code = {response.status_code} ")

class Item:
    """ Item object for an invoice """

    def __init__(self, name, quantity, unit_cost, description=""):
        """ Object constructor """
        self.name = name
        self.quantity = quantity
        self.unit_cost = unit_cost
        self.description = description


# EXAMPLE
invoice = InvoiceGenerator(
    to="Kristin",
    number=1,
    amount_paid=0,
)

invoice.add_item(
    name="Clean",
    quantity=1,
    unit_cost=99,
)
invoice.add_item(
    name="Oven Deep Clean",
    quantity=1,
    unit_cost=25,
)

invoice.download("test_invoice.pdf")
