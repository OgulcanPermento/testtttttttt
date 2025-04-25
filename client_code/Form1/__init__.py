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
        self.data_grid_4.rows_per_page = 20
      
        self.sort_state_1 = {}
        self.link_map = {
            'column_1': self.link_1,
            'column_2': self.link_2,
            'column_3': self.link_3,
            'column_4': self.link_4,
            'column_5': self.link_5,
            'column_6': self.link_6,
            'column_7': self.link_7,
            'column_8': self.link_8,
            'column_9': self.link_9,
            'column_10': self.link_10,
            'column_11': self.link_11,
            'column_12': self.link_12,
            'column_13': self.link_13,
            'column_14': self.link_14
        }

        self.link_1.icon = 'fa:caret-down'
        self.link_2.icon = 'fa:sort'
        self.link_3.icon = 'fa:sort'
        self.link_4.icon = 'fa:sort'
        self.link_5.icon = 'fa:caret-down'
        self.link_6.icon = 'fa:sort'
        self.link_7.icon = 'fa:sort'
        self.link_8.icon = 'fa:sort'
        self.link_9.icon = 'fa:sort'
        self.link_10.icon = 'fa:caret-down'
        self.link_11.icon = 'fa:sort'
        self.link_12.icon = 'fa:sort'
        self.link_13.icon = 'fa:sort'
        self.link_14.icon = 'fa:sort'

    def strdate_to_numdate(self, strdate):
        return datetime.combine(strdate, datetime.min.time())

    def strdate_to_end_of_day(self, strdate):
        return datetime.combine(strdate, datetime.max.time())
      
    def form_refreshing_data_bindings(self, **event_args):
        pass

    def search_box_1_change(self, **event_args):
        self.filter_email_stats()  # Filter voor repeating_panel_1

    def search_box_4_change(self, **event_args):
        self.filter_assessor_info()

    def search_box_change(self, **event_args):
        self.filter_handelingen()

    def start_date_change(self, **event_args):
        self.num_startdate = self.strdate_to_numdate(self.start_date.date)
        self.plot_1_show()
        self.plot_2_show()
        self.plot_3_show()
        self.data_grid_1_show()
        self.data_grid_3_show()
        self.data_grid_4_show()

    def end_date_change(self, **event_args):
        self.num_enddate = self.strdate_to_end_of_day(self.end_date.date)
        self.plot_1_show()
        self.plot_2_show()
        self.plot_3_show()
        self.data_grid_1_show()
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
        try:
            data = anvil.server.call('get_email_stats', self.num_startdate, self.num_enddate)
            sorted_data = sorted(data, key=lambda x: str(x['achternaam']).lower())
            self.repeating_panel_1.items = sorted_data
            self.repeating_panel_1.tag = sorted_data
        except Exception as e:
            print(f"Fout bij het ophalen van assessor informatie: {e}")
            alert(f"Fout bij het ophalen van assessor informatie: {e}")

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

    def filter_email_stats(self, **event_args):
        zoekterm = self.search_box_1.text.lower()  # Aangepast zoekvak voor repeating_panel_1
        originele_data_1 = self.repeating_panel_1.tag

        # Controleer of de tag geen None is en of het een lijst is
        if not isinstance(originele_data_1, list):
            return  # Als de tag geen lijst is, stop dan

        if originele_data_1 is None:
            return

        if not zoekterm or len(zoekterm) < 2:
            self.repeating_panel_1.items = originele_data_1
            return

        # Filter de resultaten op basis van de zoekterm
        gefilterde_resultaten_1 = []
        for item in originele_data_1:
            if item.get('achternaam', '').lower().startswith(zoekterm) or item.get('voornaam', '').lower().startswith(zoekterm):
                gefilterde_resultaten_1.append(item)

        # Stel de gefilterde items in
        self.repeating_panel_1.items = gefilterde_resultaten_1

    def filter_assessor_info(self, **event_args):
        zoekterm = self.search_box_4.text.lower()  # Aangepast zoekvak voor repeating_panel_4
        originele_data_4 = self.repeating_panel_4.tag

        if originele_data_4 is None:
            return

        if not zoekterm or len(zoekterm) < 2:
            self.repeating_panel_4.items = originele_data_4
            return

        gefilterde_resultaten_4 = []
        for item in originele_data_4:
            if item.get('achternaam', '').lower().startswith(zoekterm) or item.get('voornaam', '').lower().startswith(zoekterm):
                gefilterde_resultaten_4.append(item)

        self.repeating_panel_4.items = gefilterde_resultaten_4

    def link_click(self, **event_args):
        # Toggle icon
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

        # Reset icons of other links
        for link in self.link_map.values():
            if link != event_args['sender']:
                link.icon = 'fa:sort'

        reverse = event_args['sender'].icon == 'fa:caret-up'

        # Sort repeating_panel_3 (Handelingen)
        if clicked_column in ['column_1', 'column_2', 'column_3', 'column_4']:
            current_data = self.repeating_panel_3.items

            if clicked_column == 'column_1':
                sorted_data = sorted(current_data, key=lambda k: str(k['handeling']).lower(), reverse=reverse)
            elif clicked_column == 'column_2':
                sorted_data = sorted(current_data, key=lambda k: k['aantal_handeling_checks'], reverse=reverse)
            elif clicked_column == 'column_3':
                sorted_data = sorted(current_data, key=lambda k: k['aantal_failed'], reverse=reverse)
            elif clicked_column == 'column_4':
                sorted_data = sorted(current_data, key=lambda k: k['aantal_passed'], reverse=reverse)

            self.repeating_panel_3.items = sorted_data

        # Sort repeating_panel_1 (Email stats)
        elif clicked_column in ['column_5', 'column_6', 'column_7', 'column_8', 'column_9']:
            current_data = self.repeating_panel_1.items

            if clicked_column == 'column_5':
                sorted_data = sorted(current_data, key=lambda k: str(k['achternaam']).lower(), reverse=reverse)
            elif clicked_column == 'column_6':
                sorted_data = sorted(current_data, key=lambda k: k['voornaam'], reverse=reverse)
            elif clicked_column == 'column_7':
                sorted_data = sorted(current_data, key=lambda k: k['email-adres'], reverse=reverse)
            elif clicked_column == 'column_8':
                sorted_data = sorted(current_data, key=lambda k: k['locatie'], reverse=reverse)
            elif clicked_column == 'column_9':
                sorted_data = sorted(current_data, key=lambda k: k['count'], reverse=reverse)

            self.repeating_panel_1.items = sorted_data

        # Sort repeating_panel_4 (Assessor info)
        elif clicked_column in ['column_10', 'column_11', 'column_12', 'column_13', 'column_14']:
            current_data = self.repeating_panel_4.items

            if clicked_column == 'column_10':
                sorted_data = sorted(current_data, key=lambda k: str(k['achternaam']).lower(), reverse=reverse)
            elif clicked_column == 'column_11':
                sorted_data = sorted(current_data, key=lambda k: k['voornaam'], reverse=reverse)
            elif clicked_column == 'column_12':
                sorted_data = sorted(current_data, key=lambda k: k['email-adres'], reverse=reverse)
            elif clicked_column == 'column_13':
                sorted_data = sorted(current_data, key=lambda k: k['locatie'], reverse=reverse)
            elif clicked_column == 'column_14':
                sorted_data = sorted(current_data, key=lambda k: k['count'], reverse=reverse)

            self.repeating_panel_4.items = sorted_data
