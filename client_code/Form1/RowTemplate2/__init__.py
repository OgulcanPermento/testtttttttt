from ._anvil_designer import RowTemplate2Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class RowTemplate2(RowTemplate2Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def column_5_click(self, **event_args):
    """This method is called when the link is clicked"""
    alert(f"{self.item['voornaam']} {self.item['achternaam']} heeft {self.item['count']} checks afgenomen")

  def column_6_click(self, **event_args):
    """This method is called when the link is clicked"""
    alert(f"{self.item['voornaam' ]} {self.item['achternaam']} heeft {self.item['count']} checks afgenomen")

  def column_7_click(self, **event_args):
    """This method is called when the link is clicked"""
    alert(f"{self.item['voornaam' ]} {self.item['achternaam']} heeft {self.item['count']} checks afgenomen")

  def column_8_click(self, **event_args):
    """This method is called when the link is clicked"""
    alert(f"{self.item['voornaam' ]} {self.item['achternaam']} heeft {self.item['count']} checks afgenomen")

  def column_9_click(self, **event_args):
    """This method is called when the link is clicked"""
    alert(f"{self.item['voornaam' ]} {self.item['achternaam']} heeft {self.item['count']} checks afgenomen")
