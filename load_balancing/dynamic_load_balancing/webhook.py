from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/alert', methods=['POST'])
def alert():
    alert_data = request.json
    instance = alert_data['alerts'][0]['labels']['instance']
    
    # Trigger Ansible playbook to adjust HAProxy
    os.system('ansible-playbook -i hosts.ini adjust_haproxy.yml --extra-vars "instance={}"'.format(instance))
    
    return "Alert received", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
