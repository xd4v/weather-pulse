import requests
from operator import itemgetter
from datetime import datetime, timedelta


def decode_cloud_cover(cloud_level, precipitation):
    # rains
    if precipitation > 2: 
        if cloud_level < 50:
            return '🌦'
        else: 
            return '🌧'
    # doesnt rain
    else: 
        if cloud_level >= 0 and cloud_level < 10 and precipitation < 0.2:
            return '☀️'
        elif cloud_level >= 10 and cloud_level < 25:
            return '🌤'
        elif cloud_level >= 25 and cloud_level < 50:
            return '⛅️'
        elif cloud_level >= 50 and cloud_level < 90:
            return '⛅️'
        else:
            return '☁️'


def build_url(latitude, longitude, start_date, end_date):
    url = 'https://api.open-meteo.com/v1/forecast'
    
    url += f'?latitude={latitude}'
    url += f'&longitude={longitude}'
    url += f'&start_date={start_date}'
    url += f'&end_date={end_date}'
    url += '&hourly=temperature_2m,relativehumidity_2m,windspeed_10m,cloudcover,precipitation'
    url += '&daily=temperature_2m_max,temperature_2m_min,apparent_temperature_max,apparent_temperature_min,precipitation_sum,sunrise,sunset'
    url += '&timezone=Europe%2FBerlin'

    return url


def build_iso_dates():
    start = datetime.today()
    end = start + timedelta(days=1)
    return start.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d')

def format_time(time):
    day, hour = time.split('T')

    start, end = build_iso_dates()

    if day == start:
        day = 'Today'
    elif day == end:
        day = 'Tomorrow'

    return day, hour

def format(response):
    data = response.json()
    temp_unit, humidity_unit, windspeed_unit, cloudcover_unit, precipitation_unit = itemgetter(
        'temperature_2m', 'relativehumidity_2m', 'windspeed_10m', 'cloudcover', 'precipitation'
    )(data['hourly_units'])
    
    # today's summary
    daily = data['daily']
    temp_min_air = daily['temperature_2m_min'][0]
    temp_max_air = daily['temperature_2m_max'][0]
    temp_min_felt = daily['apparent_temperature_min'][0]
    temp_max_felt = daily['apparent_temperature_max'][0]
    total_preci = daily['precipitation_sum'][0]
    sunrise = daily['sunrise'][0]
    sunset = daily['sunset'][0]
    
    weather_report = '<div style="width: 100%; text-align: left;">'
    weather_report += f'''
        <p>
            Today's weather:
            <ul>
                <li>Min temperature: <b>{temp_min_air}</b>{temp_unit} (felt: <b>{temp_min_felt}</b>{temp_unit})</li>
                <li>Max temperature: <b>{temp_max_air}</b>{temp_unit} (felt: <b>{temp_max_felt}</b>{temp_unit})</li>
                <li>Total rain: <b>{total_preci}</b>{precipitation_unit}</li>
                <li>Sunrise: <b>{sunrise.split('T')[1]}</b></li>
                <li>Sunset: <b>{sunset.split('T')[1]}</b></li>
            </ul>
        </p>
    '''

    # table showing two next days

    hourly = data['hourly']
    time = hourly['time']
    temperatures = hourly['temperature_2m']
    humidities = hourly['relativehumidity_2m']
    windspeeds = hourly['windspeed_10m']
    cloudcover = hourly['cloudcover']
    precipitations = hourly['precipitation']
    
    weather_report += '<table style="text-align: right">'
    weather_report += '''
    <tr>
        <th style="width: 100px"></th>
        <th>temperature</th>
        <th></th>
        <th>cloud cover</th>
        <th>precipitation</th>
        <th>windspeed</th>
        <th>humidity</th>
    </tr>
    '''
    for i, t in enumerate(time):
        temp = temperatures[i]
        humidity = humidities[i]
        windspeed = windspeeds[i]
        cloud = cloudcover[i]
        preci = precipitations[i]

        day, hour = format_time(t)
        weather_report += f'''
        <tr>
            <td style="min-width: 100px">{day}\n{hour}</td>
            <td style="min-width: 40px">{temp}{temp_unit}</td>
            <td style="min-width: 40px">{decode_cloud_cover(cloud, preci)}</td>
            <td style="min-width: 40px">{cloud}{cloudcover_unit}</dh
            <td style="min-width: 40px">{preci}{precipitation_unit}</td>
            <td style="min-width: 40px">{windspeed}{windspeed_unit}</td>
            <td style="min-width: 40px">{humidity}{humidity_unit}</td>

        </tr>
        '''

    weather_report += '</table>'
    weather_report += '</div>'

    print(weather_report)
    return weather_report


def run():
    start, end = build_iso_dates()
    response = requests.get(build_url('48.9119', '2.3338', start, end))
    return format(response)


run()