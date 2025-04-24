from ._anvil_designer import RowTemplate4Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class RowTemplate4(RowTemplate4Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def form_refreshing_data_bindings(self, **event_args):
    """This method is called when refresh_data_bindings is called"""
    pass

  def column_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    alert(f"{self.item['handeling']} heeft {self.item['aantal_handeling_checks']} checks gedaan")

  def column_2_click(self, **event_args):
    """This method is called when the link is clicked"""
    alert(f"{self.item['handeling']} heeft {self.item['aantal_handeling_checks']} checks afgerond ")

  def column_3_click(self, **event_args):
    """This method is called when the link is clicked"""
    alert(f"{self.item['handeling']} is {self.item['aantal_failed']} keer gefaald ")

  def column_4_click(self, **event_args):
    """This method is called when the link is clicked"""
    alert(f"{self.item['handeling']} is {self.item['aantal_passed']} keer geslaagd ")

  



