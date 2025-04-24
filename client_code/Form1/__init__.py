from ._anvil_designer import Form1Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import plotly.graph_objects as go
from datetime import datetime, timedelta, date
from time import time

class Form1(Form1Template): 

    def __init__(self, **properties):
        self.init_components(**properties)

        self.end_date.date = date.today()
        self.num_enddate = self.strdate_to_end_of_day(self.end_date.date)
        end_date = self.end_date.date

        if end_date.month == 1:
            new_month = 12
            new_year = end_date.year - 1
        else:
            new_month = end_date.month - 1
            new_year = end_date.year

        start_date = date(new_year, new_month, 1)
        self.start_date.date = start_date
        self.num_startdate = self.strdate_to_numdate(self.start_date.date)
      
        self.sort_state_1 = {}
        self.link_map = {
            'column_1': self.link_1,
            'column_2': self.link_2,
            'column_3': self.link_3,
            'column_4': self.link_4
        }

        self.link_1.icon = 'fa:caret-down'
        self.link_2.icon = 'fa:sort'
        self.link_3.icon = 'fa:sort'
        self.link_4.icon = 'fa:sort'

    def strdate_to_numdate(self, strdate):
        return datetime.combine(strdate, datetime.min.time())

    def strdate_to_end_of_day(self, strdate):
        return datetime.combine(strdate, datetime.max.time())
      
    def form_refreshing_data_bindings(self, **event_args):
        pass

    def search_box_pressed_enter(self, **event_args):
        self.filter_handelingen()

    def search_box_change(self, **event_args):
        self.filter_handelingen()

    def start_date_change(self, **event_args):
        self.num_startdate = self.strdate_to_numdate(self.start_date.date)
        self.plot_1_show()
        self.plot_2_show()
        self.plot_3_show()
        self.data_grid_1_show()
        self.data_grid_2_show()
        self.data_grid_3_show()
        self.data_grid_4_show()

    def end_date_change(self, **event_args):
        self.num_enddate = self.strdate_to_end_of_day(self.end_date.date)
        self.plot_1_show()
        self.plot_2_show()
        self.plot_3_show()
        self.data_grid_1_show()
        self.data_grid_2_show()
        self.data_grid_3_show()
        self.data_grid_4_show()

    def plot_1_show(self, **event_args):
        location_results = anvil.server.call('get_teams', self.num_startdate, self.num_enddate)
        locations = list(location_results.keys())
        passed_values = [location_results[loc]['passed'] for loc in locations]
        failed_values = [location_results[loc]['failed'] for loc in locations]

        passed_bar = go.Bar(
            x=locations,
            y=passed_values,
            name='Passed',
            marker_color='lightblue'
        )

        failed_bar = go.Bar(
            x=locations,
            y=failed_values,
            name='Failed',
            marker_color='darkblue'
        )

        layout = go.Layout(
            title={
                'text': 'Assessment Resultaten per Locatie',
                'x': 0.045,
                'font': dict(family="Arial", size=12, color='#333333')
            },
            margin=dict(t=50, l=50, r=50, b=60),
            barmode='group',
            bargap=0.2,
        )

        self.plot_1.data = [passed_bar, failed_bar]
        self.plot_1.layout = layout

    def plot_2_show(self, **event_args):
        passed, failed = anvil.server.call('get_results', self.num_startdate, self.num_enddate)

        self.plot_2.data = go.Pie(
            labels=['Passed', 'Failed'],
            values=[passed, failed],
            showlegend=False,
            textposition='inside',
            textinfo='label+value',
            marker=dict(
                colors=['lightblue', 'darkblue'],
                line=dict(width=1, color='#FFFFFF')
            )
        )

        self.plot_2.layout = go.Layout(
            title={
                'text': 'Geslaagd en Niet Geslaagd',
                'x': 0.045,
                'font': dict(family="Arial", size=12, color='#333333')
            },
            margin=dict(t=50, l=50, r=50, b=50),
        )

    def plot_3_show(self, **event_args):
        dates, counts = anvil.server.call('get_dates', self.num_startdate, self.num_enddate)

        self.plot_3.data = [
            go.Scatter(
                x=dates,
                y=counts,
                mode='lines+markers',
                line=dict(color='darkblue'),
                marker=dict(color='darkblue')
            )
        ]

        self.plot_3.layout = go.Layout(
            title={
                'text': 'Collegiale checks over periode',
                'x': 0.045,
                'font': dict(family="Arial", size=12, color='#333333')
            },
            margin=dict(t=50, l=50, r=50, b=60)
        )

    def data_grid_1_show(self, **event_args):
        self.repeating_panel_1.items = anvil.server.call('get_email_stats', self.num_startdate, self.num_enddate)

    def data_grid_2_show(self, **event_args):
        self.repeating_panel_2.items = anvil.server.call('get_assessor_info', self.num_startdate, self.num_enddate)

    def data_grid_3_show(self, **event_args):
        handeling_result = anvil.server.call('get_handeling_stats', self.num_startdate, self.num_enddate)
        sorted_data = sorted(handeling_result, key=lambda k: str(k['handeling']).lower())
        self.repeating_panel_3.items = sorted_data
        self.repeating_panel_3.tag = sorted_data

    def data_grid_4_show(self, **event_args):
      try:
          data = anvil.server.call('get_assessor_info', self.num_startdate, self.num_enddate)
          sorted_data = sorted(data, key=lambda x: str(x['achternaam']).lower())
          self.repeating_panel_4.items = sorted_data
          self.repeating_panel_4.tag = sorted_data
      except Exception as e:
          print(f"Fout bij het ophalen van assessor informatie: {e}")
          alert(f"Fout bij het ophalen van assessor informatie: {e}")

    def filter_handelingen(self, **event_args):
        zoekterm = self.search_box.text.lower()
        originele_data = self.repeating_panel_3.tag

        if originele_data is None:
            return

        if not zoekterm or len(zoekterm) < 2:
            self.repeating_panel_3.items = originele_data
            return

        gefilterde_resultaten = []
        for item in originele_data:
            if item['handeling'].lower().startswith(zoekterm):
                gefilterde_resultaten.append(item)

        self.repeating_panel_3.items = gefilterde_resultaten

    def link_click(self, **event_args):
        if event_args['sender'].icon == 'fa:caret-down':
            event_args['sender'].icon = 'fa:caret-up'
        elif event_args['sender'].icon == 'fa:caret-up':
            event_args['sender'].icon = 'fa:caret-down'
        else:
            event_args['sender'].icon = 'fa:caret-down'

        clicked_column = None
        for column, link in self.link_map.items():
            if link == event_args['sender']:
                clicked_column = column
                break

        for link in self.link_map.values():
            if link != event_args['sender']:
                link.icon = 'fa:sort'

        current_data = self.repeating_panel_3.items

        if clicked_column == 'column_1':
            sorted_data = sorted(current_data, key=lambda k: str(k['handeling']).lower(), reverse=event_args['sender'].icon == 'fa:caret-up')
        elif clicked_column == 'column_2':
            sorted_data = sorted(current_data, key=lambda k: k['aantal_handeling_checks'], reverse=event_args['sender'].icon == 'fa:caret-up')
        elif clicked_column == 'column_3':
            sorted_data = sorted(current_data, key=lambda k: k['aantal_failed'], reverse=event_args['sender'].icon == 'fa:caret-up')
        elif clicked_column == 'column_4':
            sorted_data = sorted(current_data, key=lambda k: k['aantal_passed'], reverse=event_args['sender'].icon == 'fa:caret-up')
        else:
            sorted_data = current_data

        self.repeating_panel_3.items = sorted_data

    


