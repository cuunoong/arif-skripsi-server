import asyncio
import sys
import websockets
import Skripsi
import json

phone = None
car = None
running = False

PID = Skripsi.pid()

async def server(websocket, path):
    global phone
    global car
    global running
    global PID
    lane = Skripsi.lane()

    try:
        async  for message in websocket:
            
            # Initialize phone ws
            if message == "PHONE":
                print("Phone connected")
                phone = websocket
                if(car is not None):
                    await phone.send("CAR")

            # Initialize car ws
            if message == "CAR":
                print("Car connected")
                car = websocket
                if(phone is not None):
                    await phone.send("CAR")

            if websocket == phone:
                if car is not None:
                    
                    if message == "RUN":
                        print("Yok maju")
                        running = True
                        await car.send("{\"ACTION\" : \"RUN\", \"DEG\" : 90}")
                    elif message == "STOP":
                        print("Stop")
                        running = False
                        await car.send("{\"ACTION\": \"STOP\"}")
            else:
                if phone is not None:
                    if type(message) is bytes:
                        image = lane.setImage(message)
                        lane.save()
                        color = lane.colorSelection(image)
                        gray = lane.grayscale(color)
                        gaussian = lane.gaussianBlur(gray)
                        edge = lane.cannyEdgeDetection(gaussian)
                        roi = lane.regionSelection(edge)
                        hough = lane.houghTransform(roi)
                        
                        await phone.send(lane.getImage(lane.drawLaneLines(image, lane.lane_lines(image, hough))))
                            # await detectLine(message)
                    else:
                        await phone.send(message)
    except:
        print("Unexpected error:", sys.exc_info()[0])

    finally:
        running = False
        if websocket == phone:
            print("Phone Disconected")
            phone = None
            

        if websocket == car:
            print("Car Disconected")
            car = None
            if(phone is not None):
                    await phone.send("CAR DISCONNECTED")


start_server = websockets.serve(server, "192.168.73.233", 5000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

