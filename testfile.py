import sysv_ipc

key = 1234
mq = sysv_ipc.MessageQueue(key)
ms, t = mq.receive()

print(ms)

