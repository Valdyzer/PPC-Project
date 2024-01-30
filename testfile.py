import sysv_ipc

key = 1234
mq = sysv_ipc.MessageQueue(key)


print(mq.current_messages)

