import urllib3
import json

http = urllib3.PoolManager()

def composeMsg(msg, alarm):
    if alarm == "ALARM":
        alarmName = json.loads(msg['Records'][0]['Sns']['Message'])
        message = str(
            "*Alarm Name:* " + "`" + alarmName['AlarmName'] + "`" + 
            "\n*Status:* " + "`" + alarmName['NewStateValue'] + "`" + 
            "\n*Description:* " + "Health check is unhealthy!" + 
            "\n*Timestamp:* " + msg['Records'][0]['Sns']['Timestamp'] + 
            "\n*Details:*" + "```" + alarmName['NewStateReason'] + "```" 
            "\n*Alarm Link:* " + "https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#alarmsV2:alarm/" + alarmName['AlarmName'])
        return message
    if alarm == "OK":        
        alarmName = json.loads(msg['Records'][0]['Sns']['Message'])
        message = str(
            "*Alarm Name:* " + "`" + alarmName['AlarmName'] + "`" + 
            "\n*Status:* " + "`" + alarmName['NewStateValue'] + "`" + 
            "\n*Description:* " + "Health check is healthy!" + 
            "\n*Timestamp:* " + msg['Records'][0]['Sns']['Timestamp'] + 
            "\n*Details:*" + "```" + alarmName['NewStateReason'] + "```" 
            "\n*Alarm Link:* " + "https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#alarmsV2:alarm/" + alarmName['AlarmName'])
        return message

def lambda_handler(event, context):
    url = "<PUT_YOUR_SLACK_WEBHOOK_URL>"

    responseStatus = str(event['Records'][0]['Sns']['Subject'])
    if "ALARM" in responseStatus:
        title = str("*" + event['Records'][0]['Sns']['Subject'] + "*")
        slackMsg = composeMsg(event, "ALARM")
        msg = {
            "channel": "<CHANNEL_NAME>",
            "text": title,
            "attachments": [{
                "color": "#961e13",
                "fields": [{
                    "value": slackMsg,
                }]
            }]
            
        }
    
    if "OK" in responseStatus:
        title = str("*" + event['Records'][0]['Sns']['Subject'] + "*")
        slackMsg = composeMsg(event, "OK")
        msg = {
            "channel": "<CHANNEL_NAME>",
            "text": title,
            "attachments": [{
                "color": "#5cb589",
                "fields": [{
                    "value": slackMsg,
                }]
            }]
            
        }
    encoded_msg = json.dumps(msg).encode('utf-8')
    resp = http.request('POST',url, body=encoded_msg)
    print({
        "message": event['Records'][0]['Sns']['Message'], 
        "status_code": resp.status, 
        "response": resp.data
    })
