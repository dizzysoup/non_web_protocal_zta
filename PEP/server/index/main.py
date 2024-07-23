from ssh_server import run_servers
from grpc_server import start_gGPC_server
from RDP_server import run_rdpservers
import threading
import logging


while True :
    
    
    # port 2223
    ssh_thread = threading.Thread(target=run_servers,daemon=True)
    # port 50051
    grpc_thread = threading.Thread(target=start_gGPC_server, daemon=True)
    # port 3389
    rdp_thread = threading.Thread(target=run_rdpservers, daemon=True)
    
    ssh_thread.start()
    grpc_thread.start()
    rdp_thread.start()
    
    ssh_thread.join()    
    grpc_thread.join()
    rdp_thread.join()
    



    
    

   


