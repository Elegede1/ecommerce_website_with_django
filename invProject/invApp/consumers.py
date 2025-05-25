import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

# A unique group name for broadcasting.
# You might have multiple groups for different types of streams.
STREAM_GROUP_NAME = "live_stream_group"

class StreamConsumer(WebsocketConsumer):
    def connect(self):
        """
        Called when the websocket is trying to connect.
        """
        # Add this channel to the group
        async_to_sync(self.channel_layer.group_add)(
            STREAM_GROUP_NAME,
            self.channel_name
        )
        self.accept() # Accept the connection
        print(f"WebSocket connected: {self.channel_name} to group {STREAM_GROUP_NAME}")

        # Optionally, send a welcome message or initial data
        # self.send(text_data=json.dumps({
        #     'type': 'connection_established',
        #     'message': 'You are now connected to the live stream!'
        # }))

    def disconnect(self, close_code):
        """
        Called when the WebSocket closes for any reason.
        """
        # Remove this channel from the group
        async_to_sync(self.channel_layer.group_discard)(
            STREAM_GROUP_NAME,
            self.channel_name
        )
        print(f"WebSocket disconnected: {self.channel_name} from group {STREAM_GROUP_NAME}")

    def receive(self, text_data):
        """
        Called when the server receives a message from the WebSocket.
        (Primarily for client-to-server communication)
        """
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message')
        print(f"Received message from client {self.channel_name}: {message}")

        # Example: Echo message back to the group (or process it)
        # async_to_sync(self.channel_layer.group_send)(
        #     STREAM_GROUP_NAME,
        #     {
        #         'type': 'stream_message', # This will call the stream_message method
        #         'message': f"Client said: {message}"
        #     }
        # )

    # Custom handler for messages sent to the group
    def stream_message(self, event):
        """
        Handles messages sent to the group with type 'stream_message'.
        This method name matches the 'type' in group_send.
        """
        message = event['message']
        payload = event.get('payload', {}) # Optional additional data

        print(f"Sending message to client {self.channel_name}: {message}, payload: {payload}")
        # Send message to WebSocket client
        self.send(text_data=json.dumps({
            'message': message,
            'payload': payload
        }))

# Helper function to send messages from outside the consumer (e.g., from a Django view)
def send_live_update(message_content, payload_data=None):
    from channels.layers import get_channel_layer
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        STREAM_GROUP_NAME,
        {
            "type": "stream_message", # This will call the stream_message method in the consumer
            "message": message_content,
            "payload": payload_data if payload_data is not None else {}
        }
    )
    print(f"Sent update to group {STREAM_GROUP_NAME}: {message_content}")