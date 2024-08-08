import json
import requests
from datetime import datetime, timedelta


def transform_time_to_clock(time_str):
    time_obj = datetime.fromisoformat(time_str.replace("Z", "+00:00"))
    return [time_obj.strftime("%H"), time_obj.strftime("%M")]


def transform_time_to_timer(time_str):
    time_obj = datetime.fromisoformat(time_str.replace("Z", "+00:00"))
    time_left = time_obj - datetime.utcnow()
    hours, remainder = divmod(time_left.total_seconds(), 3600)
    minutes, _ = divmod(remainder, 60)
    return [f"{int(hours)}t", f"{int(minutes)} min"]


def lambda_handler(event, context):
    stop_place = event['queryStringParameters']['stopPlace']
    URL = event['queryStringParameters']['URL']

    query = """
        query ($stopPlace: String!) {
            stopPlace(id: $stopPlace) {
                estimatedCalls(numberOfDepartures: 3) {
                    expectedDepartureTime
                    date
                }
            }
        }
    """

    variables = {"stopPlace": stop_place}
    headers = {
        'Content-Type': 'application/json',
        'ET-Client-Name': 'ArmandYoussefianBlakstvedt-RandsfjordsferjaRutetabell',
    }

    response = requests.post(
        URL, json={'query': query, 'variables': variables}, headers=headers)
    data = response.json().get('data', {}).get(
        'stopPlace', {}).get('estimatedCalls', [])

    route_times = []
    times_left = []

    for element in data:
        route_times.append(transform_time_to_clock(
            element['expectedDepartureTime']))
        times_left.append(transform_time_to_timer(
            element['expectedDepartureTime']))

    return {
        'statusCode': 200,
        'body': json.dumps([route_times, times_left]),
        'headers': {
            'Content-Type': 'application/json',
        }
    }
