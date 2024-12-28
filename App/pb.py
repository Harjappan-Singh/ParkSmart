from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.models.consumer.v3.channel import Channel
import os

CHANNEL_NAME = os.getenv('PUBNUB_CHANNEL')
# PubNub configuration
def initialize_pubnub(uuid):
    if not uuid:
        raise ValueError("UUID cannot be empty or None.")
    
    pnconfig = PNConfiguration()
    pnconfig.subscribe_key = os.getenv('PUBNUB_SUBSCRIBE_KEY')
    pnconfig.publish_key = os.getenv('PUBNUB_PUBLISH_KEY')
    pnconfig.secret_key = os.getenv('PUBNUB_SECRET_KEY')
    pnconfig.uuid = uuid
    return PubNub(pnconfig)

    
def generate_token(user_id, ttl=60):
    try:
        pubnub = initialize_pubnub(user_id)
        
        # print(f"Granting token for user_id: {user_id}")
        
        envelope = pubnub.grant_token() \
            .channels([Channel.id(CHANNEL_NAME).read().write()]) \
            .authorized_uuid(user_id) \
            .ttl(ttl) \
            .sync() 
        
        token = envelope.result.token 
        print(token)
        return token
    except Exception as e:
        print(f"Error generating token: {e}")
        return None

def refresh_token(user_id, ttl=60):
    try:
        new_token = generate_token(user_id, ttl=ttl)
        return new_token
    except Exception as e:
        print(f"Error in refresh_token: {e}")
        return None