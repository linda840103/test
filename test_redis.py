import redis
import cv2
#import struct
import numpy as np
import time


def displayframe(cap, r1, r2, cmds):

		ret, frame = cap.read()
		frame = cv2.resize(frame, (640, 360))
		#cv2.imshow('Input', frame)
		retval, frameBuf = cv2.imencode('.png', frame)
		frameStr = np.array(frameBuf).tostring()
		
		r1.publish("foo", frame.tobytes())
		r2.set("bar", frameStr)
		
		for item in p1.listen():
				if item["type"] == "message":
						decodeStr1 = item["data"]
						break
		
		decodeStr2 = r2.get("bar")
		frame1 = np.frombuffer(decodeStr1, dtype="uint8").reshape(360, 640, 3)				
		frame2 = cv2.imdecode(np.frombuffer(decodeStr2, np.uint8), 1)
		
		if cmds == 1:										# add transparency
				shapes = np.zeros_like(frame1, np.uint8)
				x, y, w, h = 0, 0, 640, 360  # Rectangle parameters
				cv2.rectangle(shapes, (x, y), (x+w, y+h), (255, 255, 255), cv2.FILLED)  # A filled rectangle
				alpha = 0.05
				frame1 = cv2.addWeighted(shapes, alpha, frame1, 1 - alpha, 0)
				frame2 = cv2.addWeighted(shapes, alpha, frame2, 1 - alpha, 0)

		elif cmds == 2:									# rotate 90 deg clockwise
				frame2 = cv2.rotate(frame2, cv2.ROTATE_90_CLOCKWISE)
		elif cmds == 3:									# mirror frame
				frame1 = cv2.flip(frame1,1)
		
		cv2.imshow("foo", frame1)	
		cv2.imshow('bar', frame2)
		

if __name__ == '__main__':
    
		r1 = redis.Redis(host='localhost', port=6379, db=0)
		r2 = redis.Redis(host='localhost', port=6379, db=0)
		p1 = r1.pubsub()
		p1.subscribe("foo")
		
		cap = cv2.VideoCapture(0)
		
		counter = 1
		
		displayframe(cap, r1, r2, 0)  # Q1 to Q5
		while counter < 1001:					# the remaining questiones
				if counter % 15 == 0:
						displayframe(cap, r1, r2, 1)
				elif counter % 3 == 0:
						displayframe(cap, r1, r2, 2)
				elif counter % 5 == 0:
						displayframe(cap, r1, r2, 3)
				else:
						displayframe(cap, r1, r2, 0)
				
				counter += 1
		
				c = cv2.waitKey(1)
				if c == 27:
						break
				
		cap.release()
		p1.unsubscribe()
		cv2.destroyAllWindows()
				





