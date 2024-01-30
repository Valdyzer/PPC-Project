from multiprocessing.managers import BaseManager
import threading
import time

shared_memory = shared_memory = {"game_status": "Starting", "liste_joueurs": [1,5,3,4], "information_tokens": 0, "fuse_tokens": 3, "construction": {}}

class RemoteManager(BaseManager):
    pass

RemoteManager.register('get_shared_memory', callable=lambda: shared_memory)

def run_server():
    manager = RemoteManager(address=('localhost', 50000), authkey=b'bob')
    server_shared_memory = shared_memory
    manager.get_shared_memory = lambda: server_shared_memory
    server = manager.get_server()
    print("Server running on localhost:50000")
    server.serve_forever()

if __name__ == '__main__':
    server_thread = threading.Thread(target=run_server)
    server_thread.start()

    # Perform other tasks while the server is running
    try:
        while True:
            time.sleep(1)  # Perform other tasks here
            print("Performing other tasks...")
    except KeyboardInterrupt:
        print("Server terminated by user.")
