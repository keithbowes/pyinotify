import pyinotify

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
        if event.mask & pyinotify.IN_CLOSE_WRITE or event.mask & pyinotify.IN_CLOSE_NOWRITE:
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
        if event.mask & pyinotify.IN_MOVED_FROM:
            print(f"{pathname} moved")
            event_handled = True

        if event_handled:
            print("")
            can_finish = True
        else:
            print("Unhandled event %s on %s" % (event.maskname, event.pathname))
            print("")
        notifier._stop_event.set() # Exit when the first event(s) come in


wm = pyinotify.WatchManager()
notifier = pyinotify.ThreadedNotifier(wm,
                                     default_proc_fun=HandleEvents())
wm.add_watch('/tmp', pyinotify.ALL_EVENTS)
notifier.start()
notifier.join(timeout=60) # Wait for events up to a minute
notifier.stop()
