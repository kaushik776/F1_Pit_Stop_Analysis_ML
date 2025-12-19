import os
import numpy as np
import fastf1
from sklearn.linear_model import LinearRegression


CACHE_DIR = os.environ.get('FASTF1_CACHE_DIR', 'cache')
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

fastf1.Cache.enable_cache(CACHE_DIR)


TRACKS= [
    'Bahrain', 'Saudi Arabia', 'Australia', 'Azerbaijan', 'Miami', 'Monaco',
    'Spain', 'Canada', 'Austria', 'Great Britain', 'Hungary', 'Belgium',
    'Netherlands', 'Italy', 'Singapore', 'Japan', 'Qatar', 'USA', 'Mexico',
    'Brazil', 'Las Vegas', 'Abu Dhabi'
]

DRIVERS= [
    'VER', 'PER', 'HAM', 'RUS', 'LEC', 'SAI', 'NOR', 'PIA', 'ALO', 'STR',
    'GAS', 'OCO', 'ALB', 'SAR', 'TSU', 'RIC', 'BOT', 'ZHO', 'HUL', 'MAG'
]

YEARS= [2024, 2023, 2022, 2021]


def get_session_safe(year, track, session_type='R'):
    try:
        session = fastf1.get_session(int(year), track, session_type)
        session.load()
        return session
    except (ValueError, IndexError, KeyError) as e:
        print(f"Session load failed for {year} {track}: {e}")
        return None


def get_circuit_layout(track):
    
    session = get_session_safe(2023, track, 'Q')
    if not session:
        return None

    try:
        lap = session.laps.pick_fastest()
        telemetry = lap.get_telemetry()

        return {
            'x': telemetry['X'].tolist(),
            'y': telemetry['Y'].tolist(),
            'name': session.event.EventName
        }
    except (ValueError, KeyError, IndexError) as e:
        print(f"Layout extraction failed for {track}: {e}")
        return None


def predict_strategy(track, compound, stops):
    
    
    session = get_session_safe(2023, track, 'R')
    if not session:
        return None, "Historical data unavailable for this track."

    try:
       
        laps = session.laps.pick_quicklaps().reset_index(drop=True)
        laps = laps.dropna(subset=['LapNumber', 'LapTime'])

        
        X = laps['LapNumber'].values.reshape(-1, 1)
        y = laps['LapTime'].dt.total_seconds().values

        model = LinearRegression()
        model.fit(X, y)

        
        future_laps = np.arange(1, 58).reshape(-1, 1)
        base_pace = model.predict(future_laps)

        stops = int(stops)
        stop_penalty = 22.0  

        race_time_total = 0
        stop_laps = []

   
        if stops == 1:
            stop_laps = [25]
        elif stops == 2:
            stop_laps = [18, 38]

        for i, time in enumerate(base_pace):
            lap_num = i + 1
            adjusted_time = time

            if compound == 'SOFT':
                adjusted_time -= 0.5
            elif compound == 'HARD':
                adjusted_time += 0.5

            if lap_num in stop_laps:
                adjusted_time += stop_penalty

            race_time_total += adjusted_time

        stop_str = "No Stops"
        if stops > 0:
            stop_str = ", ".join([f"Lap {x}" for x in stop_laps])

        return {
            'total_time_min': round(race_time_total / 60, 2),
            'degradation': round(model.coef_[0], 4),
            'stop_recommendation': stop_str
        }, None

    except (ValueError, IndexError, KeyError) as e:
        return None, str(e)


def get_detailed_telemetry(year, race, d1, d2):
    
    session = get_session_safe(year, race, 'R')
    if not session:
        return None, f"Session data not found for {race} {year}"

    try:
        laps_d1 = session.laps.pick_driver(d1).pick_quicklaps() 
        laps_d2 = session.laps.pick_driver(d2).pick_quicklaps() 

        if laps_d1.empty or laps_d2.empty:
            return None, "Driver data unavailable."

        pace_data = []
        for d, laps in [(d1, laps_d1), (d2, laps_d2)]:
            df = laps[['LapNumber', 'LapTime']].copy()
            df = df.dropna()
            df['LapTime'] = df['LapTime'].dt.total_seconds()
            pace_data.append({
                'driver': d,
                'x': df['LapNumber'].tolist(),
                'y': df['LapTime'].tolist()
            })

  
        fastest_d1 = laps_d1.pick_fastest()
        fastest_d2 = laps_d2.pick_fastest()

        telemetry_data = []

        def extract_tel(lap, driver_code):
            
            try:
                tel = lap.get_telemetry()
                return {
                    'driver': driver_code,
                    'distance': tel['Distance'].tolist(),
                    'speed': tel['Speed'].tolist(),
                    'lap_time': str(lap['LapTime']).split(' days ')[-1][0:10]
                }
            except (ValueError, IndexError, KeyError):
                return None

        t1 = extract_tel(fastest_d1, d1)
        t2 = extract_tel(fastest_d2, d2)
        if t1:
            telemetry_data.append(t1)
        if t2:
            telemetry_data.append(t2)

        try:
            winner_df = session.results.loc[session.results['Position'] == 1.0]
            if winner_df.empty:
                raise IndexError("No driver found with Position 1.0")

            winner_row = winner_df.iloc[0]
            winner_info = {
                'name': winner_row['Abbreviation'],
                'team': winner_row['TeamName'],
                'time': str(winner_row['Time']).split(' days ')[-1]
            }
        except (IndexError, KeyError, ValueError) as e:
            print(f"Winner stats extraction failed: {e}")
            winner_info = {'name': 'N/A', 'team': 'N/A', 'time': 'N/A'}

        return {
            'race_name': session.event.EventName,
            'pace_data': pace_data,
            'telemetry_data': telemetry_data,
            'winner_info': winner_info
        }, None

    except (ValueError, IndexError, KeyError) as e:
        return None, str(e)
