import paho.mqtt.client as mqtt
import traceback
import psycopg2
import os

broker_source = os.environ['MQTT_HOST']
broker_source_port = int(os.environ['MQTT_PORT'])
client_source = mqtt.Client(os.environ['MQTT_CLIENT'])
client_source.username_pw_set(os.environ['MQTT_USER'], os.environ['MQTT_PWD'])

DatabaseHostName = os.environ['SQL_HOST']
DatabaseUserName = os.environ['SQL_USER']
DatabasePassword = os.environ['SQL_PWD']
DatabaseName = os.environ['SQL_DB']
DatabasePort = int(os.environ['SQL_PORT'])

print("Connecting to database")
connection = psycopg2.connect(
	host = DatabaseHostName,
	user = DatabaseUserName,
	password = DatabasePassword,
	database = DatabaseName,
	port = DatabasePort
)

def insertIntoDatabase(message):
	"Inserts the mqtt data into the database"
	with connection.cursor() as cursor:
		print("Inserting data: " + str(message.topic) + ";" + str(message.payload)[2:][:-1] + ";" + str(message.qos))
		cursor.callproc('InsertIntoMQTTTable', [str(message.topic), str(message.payload)[2:][:-1], int(message.qos)])
		connection.commit()

def on_message(client, userdata, message):
	"Evaluated when a new message is received on a subscribed topic"
	print("Received message '" + str(message.payload)[2:][:-1] + "' on topic '"
		+ message.topic + "' with QoS " + str(message.qos))
	insertIntoDatabase(message)
	
def setup():
	"Runs the setup procedure for the client"
	print("Setting up the onMessage handler")
	client_source.on_message = on_message
	print("Connecting to source")
	client_source.connect(broker_source, broker_source_port)
	client_source.subscribe("#", qos=1)
	print("Setup finished, waiting for messages...")

try:
	setup()
	client_source.loop_forever()
except Exception as e:
	traceback.print_exc()
finally:
	connection.close()
