import asyncio
import sys
import websockets
import Skripsi
import json

phone = None
car = None
running = False

PID = Skripsi.pid(90)
deg = 90
LANE = Skripsi.lane()
async def server(websocket, path):
    global phone
    global car
    global running
    global PID
    global LANE
    global deg
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
                        await car.send("{\"ACTION\" : \"RUN\", \"DEG\" : " + str(deg)+ "}")
                    elif message == "STOP":
                        print("Stop")
                        running = False
                        await car.send("{\"ACTION\": \"STOP\"}")
            else:
                if phone is not None:
                    if type(message) is bytes:
                        image = LANE.setImage(message)
                        LANE.save()
                        gray = LANE.grayscale(image)
                        blur = LANE.gaussianBlur(gray)
                        edge = LANE.cannyEdgeDetection(blur)
                        roi = LANE.regionSelection(edge)
                        lanes = LANE.getLanes(roi)
                        final = LANE.drawLaneLines(image, lanes)
                        deg = LANE.getDegree(lanes)

                        await phone.send(LANE.getImage(final))
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

