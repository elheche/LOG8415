from flask import Flask
import requests

app = Flask(__name__)

# Get ec2 instance tags to indentify the instance
cluster = requests.get('http://169.254.169.254/latest/meta-data/tags/instance/Cluster').text
instance = requests.get('http://169.254.169.254/latest/meta-data/tags/instance/Instance').text

if cluster == '1':
    route = '/cluster1'
else:
    route = '/cluster2'


@app.route('/')
@app.route(route)
def hello_from_aws():
    return {'Cluster': cluster, 'Instance': instance}
