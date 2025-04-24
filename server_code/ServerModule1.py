import anvil.server
import anvil.files
from anvil.files import data_files
from anvil.tables import app_tables, query
from datetime import datetime
import pandas as pd
import csv
import plotly.graph_objects as go

@anvil.server.callable
def get_assessor_info(begin_datum, eind_datum):
    """Haalt unieke assessor informatie op met tellingen binnen datumbereik"""
    try:
        assessments = app_tables.assessments_v2.search(
            datum=query.between(begin_datum, eind_datum)
        )
        
        assessor_data = {}
        
        for assessment in assessments:
            assessor_email = assessment.get('assessor', '')
            if not assessor_email:
                continue
            
            if assessor_email not in assessor_data:
                # Fix: gebruik **{} voor kolom met koppelteken
                person_info = app_tables.assessments.search(**{'email-adres': assessor_email})
                person = person_info[0] if person_info else None
                
                assessor_data[assessor_email] = {
                    'achternaam': person['achternaam'] if person and person['achternaam'] else '',
                    'voornaam': person['voornaam'] if person and person['voornaam'] else '',
                    'email-adres': assessor_email,
                    'locatie': person['locatie'] if person and person['locatie'] else '',
                    'count': 1
                }
            else:
                assessor_data[assessor_email]['count'] += 1
        
        result = list(assessor_data.values())
        result.sort(key=lambda x: x['achternaam'])
        
        return result
    except Exception as e:
        print(f"Fout in get_assessor_info: {e}")
        return []


@anvil.server.callable
def get_teams(begin_datum, eind_datum):
    try:
        location_results = {}
        assessments = app_tables.assessments_v2.search(
        datum=query.between(begin_datum, eind_datum)
        )
        
        for assessment in assessments:
            location = assessment.get('locatie')
            result = assessment.get('resultaat')
            
            
            if location not in location_results:
                location_results[location] = {
                    'passed': 0,
                    'failed': 0,
                    'total': 0
                }
                
            if result == 'PASSED':
                location_results[location]['passed'] += 1
            elif result == 'FAILED':
                location_results[location]['failed'] += 1
            
            location_results[location]['total'] += 1
            
        return location_results
    except Exception as e:
        print(f"Error in get_teams: {e}")
        return location_results

@anvil.server.callable
def get_results(begin_datum, eind_datum):
    try:
        assessments = app_tables.assessments_v2.search(
        datum=query.between(begin_datum, eind_datum)
        )

        passed = sum(1 for a in assessments if a.get('resultaat') == 'PASSED')
        failed = sum(1 for a in assessments if a.get('resultaat') == 'FAILED')
        return passed, failed
    except Exception as e:
        print(f"Error in get_results: {e}")
        return 0, 0

@anvil.server.callable
def get_dates(begin_datum, eind_datum):
    assessments = app_tables.assessments_v2.search(
    datum=query.between(begin_datum, eind_datum)
    )

    dates = []
    counts = []
    current_date = None
    count = 0
    
    # Sort assessments by date
    sorted_assessments = sorted(assessments, key=lambda x: x['datum'])
    
    for assessment in sorted_assessments:
        date = assessment['datum']
        
        # If new date, save previous count
        if date != current_date:
            if current_date:
                dates.append(current_date)
                counts.append(count)
            current_date = date
            count = 0
        count += 1
    
    # Add last count
    if current_date:
        dates.append(current_date)
        counts.append(count)
    
    return dates, counts

@anvil.server.callable
def get_location_plot_data():
    try:
        location_results = get_teams()
        locations = list(location_results.keys())
        passed_values = [location_results[loc]['passed'] for loc in locations]
        failed_values = [location_results[loc]['failed'] for loc in locations]
        
        fig = go.Figure(data=[
            go.Bar(x=locations, y=passed_values, name='Passed', marker_color='lightblue'),
            go.Bar(x=locations, y=failed_values, name='Failed', marker_color='darkblue')
        ])
        
        fig.update_layout(
            title={'text': 'Assessment Resultaten per Locatie', 'x': 0.045},
            margin=dict(t=50, l=50, r=50, b=60),
            barmode='group',
            bargap=0.2
        )
        
        return fig
    except Exception as e:
        print(f"Error in get_location_plot_data: {e}")
        return go.Figure(data=[go.Bar(x=['Error'], y=[0])])

@anvil.server.callable
def get_pie_plot_data():
    try:
        passed, failed = get_results()
        
        fig = go.Figure(data=[go.Pie(
            labels=['Passed', 'Failed'],
            values=[passed, failed],
            showlegend=False,
            textposition='inside',
            textinfo='label+value',
            marker=dict(colors=['lightblue', 'darkblue'], line=dict(width=1, color='#FFFFFF'))
        )])
        
        fig.update_layout(
            title={'text': 'Geslaagd en Niet Geslaagd', 'x': 0.045},
            margin=dict(t=50, l=50, r=50, b=50)
        )
        
        return fig
    except Exception as e:
        print(f"Error in get_pie_plot_data: {e}")
        return go.Figure(data=[go.Bar(x=['Error'], y=[0])])

@anvil.server.callable
def get_line_plot_data(begin_datum, eind_datum):
    try:
        dates, counts = get_dates(begin_datum, eind_datum)
        
        fig = go.Figure(data=[
            go.Scatter(
                x=dates,
                y=counts,
                mode='lines+markers',
                line=dict(color='darkblue'),
                marker=dict(color='darkblue')
            )
        ])
        
        fig.update_layout(
            title={'text': 'Collegiale checks over periode', 'x': 0.045},
            margin=dict(t=50, l=50, r=50, b=60)
        )
        
        return fig
    except Exception as e:
        print(f"Error in get_line_plot_data: {e}")
        return go.Figure(data=[go.Bar(x=['Error'], y=[0])])

@anvil.server.callable
def get_email_stats(begin_datum, eind_datum):
    try:
        assessments = app_tables.assessments_v2.search(
        datum=query.between(begin_datum, eind_datum)
        )

        email_counts = {}
        
        for assessment in assessments:
            email = assessment.get('email-adres', '')
            if not email:
                continue
                
            if email not in email_counts:
                email_counts[email] = {
                    'email-adres': email,
                    'voornaam': assessment.get('voornaam', ''),
                    'achternaam': assessment.get('achternaam', ''),
                    'locatie': assessment.get('locatie', ''),
                    'count': 1
                }
            else:
                email_counts[email]['count'] += 1
        
        return list(email_counts.values())
    except Exception as e:
        print(f"Error in get_email_stats: {e}")
        return []

@anvil.server.callable
def get_handeling_stats(begin_datum, eind_datum):
    try:
        assessments = app_tables.assessments_v2.search(
        datum=query.between(begin_datum, eind_datum)
        )

        handeling_stats = {}
        
        for assessment in assessments:
            handeling = assessment.get('handeling', '')
            resultaat = assessment.get('resultaat', '')
            
            if not handeling:
                continue
                
            if handeling not in handeling_stats:
                handeling_stats[handeling] = {
                    'handeling': handeling,
                    'aantal_handeling_checks': 1,
                    'aantal_passed': 1 if resultaat == 'PASSED' else 0,
                    'aantal_failed': 1 if resultaat == 'FAILED' else 0
                }
            else:
                handeling_stats[handeling]['aantal_handeling_checks'] += 1
                if resultaat == 'PASSED':
                    handeling_stats[handeling]['aantal_passed'] += 1
                elif resultaat == 'FAILED':
                    handeling_stats[handeling]['aantal_failed'] += 1
        
        return list(handeling_stats.values())
    except Exception as e:
        print(f"Error in get_handeling_stats: {e}")
        return []

@anvil.server.callable
def filter_handelingen(zoekterm):
    try:
        handeling_stats = get_handeling_stats()
        
        if not zoekterm or len(zoekterm) < 2:
            return handeling_stats
        
        return [item for item in handeling_stats if item['handeling'].lower().startswith(zoekterm.lower())]
    except Exception as e:
        print(f"Error in filter_handelingen: {e}")
        return []

@anvil.server.callable
def sort_handelingen(data, column, reverse):
    try:
        if column == 'column_1':
            return sorted(data, key=lambda k: str(k['handeling']).lower(), reverse=reverse)
        elif column == 'column_2':
            return sorted(data, key=lambda k: k['aantal_handeling_checks'], reverse=reverse)
        elif column == 'column_3':
            return sorted(data, key=lambda k: k['aantal_failed'], reverse=reverse)
        elif column == 'column_4':
            return sorted(data, key=lambda k: k['aantal_passed'], reverse=reverse)
        return data
    except Exception as e:
        print(f"Error in sort_handelingen: {e}")
        return data

@anvil.server.callable
def importeer_csv():
    with open(data_files['assessments_v2.csv'], "rb") as bestand:
        df = pd.read_csv(bestand, encoding="latin1", sep=";").dropna()
    
    print("Aantal rijen ingelezen:", len(df))
    rows = df.to_dict(orient="records")
    
    for row in rows:
        if 'datum' in row and isinstance(row['datum'], str):
            try:
                row['datum'] = datetime.strptime(row['datum'].strip(), "%d-%m-%Y").date()
            except Exception as e:
                print(f"Fout bij het converteren van datum in rij {row}: {e}")
                row['datum'] = None
        
        try:
            app_tables.assessments_v2.add_row(**row)
        except Exception as e:
            print("Fout bij toevoegen van rij", row, e)
            raise
    
    
    return "CSV succesvol geïmporteerd"