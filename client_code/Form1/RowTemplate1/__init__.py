from ._anvil_designer import RowTemplate1Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class RowTemplate1(RowTemplate1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def column_10_click(self, **event_args):
    """This method is called when the link is clicked"""
    alert(f"{self.item['voornaam']} {self.item['achternaam']} heeft {self.item['count']} checks uitgevoerd")

  def column_11_click(self, **event_args):
    """This method is called when the link is clicked"""
    alert(f"{self.item['voornaam']} {self.item['achternaam']} heeft {self.item['count']} checks uitgevoerd")

  def column_12_click(self, **event_args):
    """This method is called when the link is clicked"""
    alert(f"{self.item['voornaam']} {self.item['achternaam']} heeft {self.item['count']} checks uitgevoerd")

  def column_13_click(self, **event_args):
    """This method is called when the link is clicked"""
    alert(f"{self.item['voornaam']} {self.item['achternaam']} heeft {self.item['count']} checks uitgevoerd")

  def column_14_click(self, **event_args):
    """This method is called when the link is clicked"""
    alert(f"{self.item['voornaam']} {self.item['achternaam']} heeft {self.item['count']} checks uitgevoerd")