from is_msgs.image_pb2 import Image
from is_msgs.image_pb2 import ObjectAnnotations

import cv2
import numpy as np

def to_np(input_image):
    if isinstance(input_image, np.ndarray):
        output_image = input_image
    elif isinstance(input_image, Image):
        buffer = np.frombuffer(input_image.data, dtype=np.uint8)
        output_image = cv2.imdecode(buffer, flags=cv2.IMREAD_COLOR)
    else:
        output_image = np.array([], dtype=np.uint8)
    return output_image

def to_image(image, encode_format: str = ".jpeg", compression_level: float = 0.8, ) -> Image:
    if encode_format == ".jpeg":
        params = [cv2.IMWRITE_JPEG_QUALITY, int(compression_level * (100 - 0) + 0)]
    elif encode_format == ".png":
        params = [cv2.IMWRITE_PNG_COMPRESSION, int(compression_level * (9 - 0) + 0)]
    else:
        return Image()
    cimage = cv2.imencode(ext=encode_format, img=image, params=params)
    return Image(data=cimage[1].tobytes())

def unpack_image(message):
    
    if type(message) != bool:
        frame = message.unpack(Image)
        return frame
    
def unpack_detection(message):
        
        if type(message) != bool:
            detection = message.unpack(ObjectAnnotations)
            return detection
    
def drawBoundingBox(image, objsAnnotations, color=(0, 255, 0), thickness=2):
    
    bbox = objsAnnotations.objects[0].region.vertices
    
    vertices = [(bbox[0].x, bbox[0].y), (bbox[1].x, bbox[1].y), (bbox[2].x, bbox[2].y), (bbox[3].x, bbox[3].y)]   
    
    cv2.polylines(image, [np.array(vertices)], isClosed=True, color=color, thickness=thickness)

    return image