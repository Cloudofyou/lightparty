import grpc
from concurrent import futures
import time
import my_proto_pb2
import my_proto_pb2_grpc
import board
import neopixel

class RaspberryPiService(my_proto_pb2_grpc.RaspberryPiServicer):
    def ExecuteCommand(self, request, context):
        MAX_LEDS = 30
        command = request.command
        print(f"Received command: {command}")
        pixels1 = neopixel.NeoPixel(board.D18, MAX_LEDS, brightness=1)

        # Add your logic to process the command here

        if command == "lights":
            z = 1.0
            ploc = 1
            base_c1 = 0
            base_c2 = 128
            base_c3 = 0
            while z > 0:
                pixels1[ploc] = (int(base_c1 * z), int(base_c2 * z), int(base_c3 * z))
                z = z - 0.1
                ploc = ploc + 1

        if command == "lightsoff":
            pixels1.fill((0, 0, 0))

        if command == "stripcount":
            for i in range(MAX_LEDS):
                if (i % 10) == 0:
                    pixels1[i] = (255,128,0)
                else:
                    pixels1[i] = (0,128,255)

        if command == "exit":
            pixels1.fill((0, 0, 0))

        response = my_proto_pb2.CommandResponse(result="Command executed successfully")
        return response

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    my_proto_pb2_grpc.add_RaspberryPiServicer_to_server(RaspberryPiService(), server)
    server.add_insecure_port('[::]:50051')
    print("Server listening on port 50051...")
    server.start()
    try:
        while True:
            time.sleep(86400)  # One day in seconds
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()