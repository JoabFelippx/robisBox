from is_wire.core import Logger, Subscription, Message, Tracer, AsyncTransport
from streamChannel import StreamChannel

import json

from utils import to_np, to_image, drawBoundingBox, unpack_image, unpack_detection

def main():
    
    config = json.load(open('./etc/config/config.json'))
    
    servie_name = config['service_name']
    broker_uri = config['broker_uri']
        
    log = Logger(name=servie_name)    
        
    channel_camera = StreamChannel()
    channel_detection = StreamChannel()
    channel_robis = StreamChannel()

    log.info(f"Connected to broker {broker_uri}")

    subscription_camera = Subscription(channel=channel_camera) 
    subscription_camera.subscribe(topic="CameraGateway.1.Frame")
    
    subscription_detection = Subscription(channel=channel_detection, name=servie_name)
    subscription_detection.subscribe(topic="Robis.1.Detection")
    
    while True:
        msg_camera = channel_camera.consume_last()
        msg_detection = channel_detection.consume_last()
        
        if type(msg_camera) == bool or type(msg_detection) == bool:
            continue
        
        image = unpack_image(msg_camera)
        image = to_np(image)
        
        detections = unpack_detection(msg_detection)
    
        image = drawBoundingBox(image, detections)
        msg = to_image(image)
        
        robis_msg = Message()
        robis_msg.topic = config['topic']
        robis_msg.pack(msg)
        channel_robis.publish(msg)	
        
if __name__ == "__main__":
    main()
    