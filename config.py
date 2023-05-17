from flask import Flask
from keycloak import KeycloakOpenID

app = Flask(__name__)

keycloak_openid = KeycloakOpenID(server_url='http://localhost:8080/auth',
                                client_id='blue_sq',
                                realm_name='todopy',
                                client_secret_key='3QqpDJoYMFC7G8wN79dJTxq4BGakD4BR')

