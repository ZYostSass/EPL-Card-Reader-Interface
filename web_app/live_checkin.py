from threading import Lock
from database.database_init import Session

from database.user_options import checkin_user, process_badge
from . import socketio, get_card_reader
from flask_socketio import emit

thread = None
cancel = False
thread_lock = Lock()
cancel_lock = Lock()

def badge_reading_task():
    global cancel
    session = Session()
    count = 0
    while True:
        with cancel_lock:
            if cancel:
                cancel = False
                break
        socketio.sleep(.1)
        try:
            data = get_card_reader().get_data()
            if data is not None:
                badge, access = data
                badge = process_badge(badge)
                checkin_user(badge, session)
                socketio.emit('found_badge', badge)
        except Exception as e:
            print(e)
                    
@socketio.event
def connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(badge_reading_task)

@socketio.event
def disconnect():
    global thread, cancel
    with thread_lock:
        with cancel_lock:
            cancel = True

        thread.join()
        thread = None

  


