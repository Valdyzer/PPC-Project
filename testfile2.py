from multiprocessing.managers import BaseManager

class RemoteManager(BaseManager): pass

RemoteManager.register('get_shared_memory')

m = RemoteManager(address=('localhost', 50000), authkey=b'bob')
m.connect()

shared_memory= m.get_shared_memory()  


print(shared_memory.get("liste_joueurs"))