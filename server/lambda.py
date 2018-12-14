import json

activity=0
jump=0

def lambda_handler(event, context):
    global activity,jump
    if event['httpMethod'] == 'POST':
        rawactivity = json.loads(event['body'])
        activity = rawactivity['activity']
        if (jump == 0):
            jump = rawactivity['jump']
        return {
            'statusCode': 200,
            'body': json.dumps(str(activity))
        }

    if event['httpMethod'] == 'GET':
        data = {'activity':activity, 'jump':jump}
        if (jump != 0):
            jump = 0;
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(data)
        }