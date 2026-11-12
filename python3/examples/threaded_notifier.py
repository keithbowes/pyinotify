import pyinotify
import os

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
        notifier._stop_event.set() # Exit when the first event(s) come in


tmpdir = (os.getenv('TMPDIR') or '/tmp')

if os.getenv('TEST'):
    open(f"{tmpdir}/.notifier_started", mode='w').close()

wm = pyinotify.WatchManager()
notifier = pyinotify.ThreadedNotifier(wm,
                                     default_proc_fun=HandleEvents())
notifier.start()
wm.add_watch(tmpdir, pyinotify.ALL_EVENTS)
notifier.join(timeout=60) # Wait for events up to a minute
notifier.stop()

if os.getenv('TEST'):
    open(f"{tmpdir}/.notifier_finished", mode='w').close()
