from move import move_function
import time
from datetime import datetime
print('follow start')
mv = move_function(1)
mv.start()
print(datetime.now())
start_time = time.time()
while True:
    time.sleep(10)
    print('moving')
    if time.time() - start_time > 40:
        mv.set_end()

    if mv.get_is_end() == 1:
        print(datetime.now())
        print('end moving')
        break
print('end')