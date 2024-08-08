import json
import requests


def lambda_handler(event, context):
    line = event['queryStringParameters']['line']
    URL = event['queryStringParameters']['URL']

    query = """
        query ($line: ID!) {
            line(id: $line) {
                situations {
                    summary {
                        value
                    }
                    description {
                        value
                    }
                    infoLinks {
                        uri
                    }
                    reportAuthority {
                        name
                    }
                    validityPeriod {
                        endTime
                        startTime
                    }
                    id
                    creationTime
                }
            }
        }
    """

    variables = {"line": line}
    headers = {
        'Content-Type': 'application/json',
        'ET-Client-Name': 'ArmandYoussefianBlakstvedt-RandsfjordsferjaRutetabell',
    }

    response = requests.post(
        URL, json={'query': query, 'variables': variables}, headers=headers)
    data = response.json().get('data', {}).get('line', {}).get('situations', [])

    if not data:
        return {
            'statusCode': 200,
            'body': json.dumps(None),
            'headers': {
                'Content-Type': 'application/json',
            }
        }

    situation = data[0]
    result = {
        'description': situation.get('description', [{}])[0].get('value', ''),
        'summary': situation.get('summary', [{}])[0].get('value', ''),
        'authority': situation.get('reportAuthority', {}).get('name', ''),
        'infoLink': situation.get('infoLinks', [{}])[0].get('uri', ''),
        'startTime': situation.get('validityPeriod', {}).get('startTime', ''),
        'endTime': situation.get('validityPeriod', {}).get('endTime', ''),
        'id': situation.get('id', ''),
        'creationTime': situation.get('creationTime', ''),
    }

    return {
        'statusCode': 200,
        'body': json.dumps(result),
        'headers': {
            'Content-Type': 'application/json',
        }
    }
