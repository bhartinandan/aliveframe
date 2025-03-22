# import cv2
# import numpy as np
# from channels.generic.websocket import AsyncWebsocketConsumer
# import base64
# import json
# from .utils import modify_frame

# class VideoStreamConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         print("connection established")
#         await self.accept()

#     async def disconnect(self, close_code):
#         pass

#     async def receive(self, text_data=None, bytes_data=None):
#         if text_data:
#             data = json.loads(text_data)
#             image_data = data.get('image')
#             if image_data:
#                 # Decode base64 image
#                 image_bytes = base64.b64decode(image_data.split(',')[1])
#                 np_arr = np.frombuffer(image_bytes, np.uint8)
#                 frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
#                 mod_frame = modify_frame(frame)
                
#                 # Convert to grayscale
#                 # gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#                 _, buffer = cv2.imencode('.jpg', mod_frame)
                
#                 # Convert processed frame to base64
#                 gray_image_base64 = base64.b64encode(buffer).decode('utf-8')
#                 await self.send(json.dumps({'image': f'data:image/jpeg;base64,{gray_image_base64}'}))
