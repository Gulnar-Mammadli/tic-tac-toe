import grpc
import random
import game_pb2
import game_pb2_grpc
import datetime
import time
from config import *
import asyncio

#import Berkeley.berkeley_utils as brkl
class Client():

    def __init__(self) -> None:
        self.serverip = "localhost"  # input("paste ip here:")
        self.reg_name = input("put your name here:")
        self.first_port = 50051
        self.channel= grpc.insecure_channel(f'{ip}:{first_port}')
        self.stub1 = game_pb2_grpc.PlayerServiceStub(self.channel)
        self.stub2 = game_pb2_grpc.AdminServiceStub(self.channel)
        self.reg_timestamp = str(datetime.datetime.now())
        self.total_processes = 3


    async def player_task(self):
        self.stub1 = game_pb2_grpc.PlayerServiceStub(self.channel)
        response = await self.stub1.player_request(game_pb2.AccessRequest(name =self.reg_name))  
        self.reg_symbol = response.symbol
        print(f"your id: {response.id} symbol {response.symbol}")

    async def list_board_async(self):
        response = await self.stub2.list_board(game_pb2.GameEmpty())
        print(response.message)
    # async def admin_task(self):
    #     self.stub2 = game_pb2_grpc.AdminServiceStub(self.channel)
    #     response = await self.stub2.admin_request(game_pb2.AdminRequest())
    #     print(response.message)

    async def run_tasks(self):
        await asyncio.gather(self.player_task())

    def access_to_server(self):
            request = game_pb2.AccessRequest()
            request.name = self.reg_name
            response = self.stub1.access_to_server(request)
            self.reg_symbol = response.symbol
            print(f"your id: {response.id} symbol {response.symbol}")  # do something with the response object
            return response
    def set_symbol(self):
            request = game_pb2.PlayerRequest()
            request.position = self.reg_position
            request.symbol = self.reg_symbol
            request.timestamp = self.reg_timestamp
            self.stub2.start_game(request)


if __name__ == "__main__": 
    a = Client()
    a.access_to_server()

    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(a.run_tasks())
