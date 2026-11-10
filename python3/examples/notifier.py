import pyinotify
import os

loop_should_terminate = False

class HandleEvents(pyinotify.ProcessEvent):
    """
    A minimal example of how to handle events.
    """
    def process_default(self, event):
        event_handled = False
        pathname = event.pathname

        if event.mask & pyinotify.IN_OPEN:
            print(f"{pathname} opened")
            event_handled = True
        if event.mask & (pyinotify.IN_CLOSE_WRITE|pyinotify.IN_CLOSE_NOWRITE):
            print(f"{pathname} closed")
            event_handled = True
        if event.mask & pyinotify.IN_CREATE:
            print(f"{pathname} was created")
            event_handled = True
        if event.mask & pyinotify.IN_DELETE:
            print(f"{pathname} was deleted")
            event_handled = True
        if event.mask & pyinotify.IN_MODIFY:
            print(f"{pathname} was modified")
            event_handled = True
        if event.mask & (pyinotify.IN_MOVED_FROM|pyinotify.IN_MOVED_TO):
            print(f"{pathname} moved")
            event_handled = True

        if event_handled:
            print("")
        else:
            print(f"Unhandled event {event.maskname} on {event.pathname}")
            print("")
        global loop_should_terminate
        loop_should_terminate = event_handled

def handle_read_callback(notifier):
    """
    Just stop receiving IO read events after the first
    iteration (unrealistic example).
    """
    print('handle_read callback')
    return loop_should_terminate


wm = pyinotify.WatchManager()

notifier = pyinotify.Notifier(wm,
                              default_proc_fun=HandleEvents())
wm.add_watch((os.getenv('TMPDIR') or '/tmp'), pyinotify.ALL_EVENTS)
notifier.loop(callback=handle_read_callback)
notifier.stop()
