import os,requests,logging
SLACK_WEBHOOK=os.getenv('SLACK_WEBHOOK_URL')
def send_slack_alert(message,severity='warning'):
    if not SLACK_WEBHOOK: return
    emoji=':red_circle:' if severity=='critical' else ':warning:'
    response=requests.post(SLACK_WEBHOOK,json={'text':f'{emoji} *Data Pipeline Alert*','attachments':[{'text':message,'color':'danger' if severity=='critical' else 'warning'}]},timeout=10)
    if response.status_code!=200: logging.error('Slack alert delivery failed: %s',response.text)
