import pyinotify
import asyncio

class HandleEvents(pyinotify.ProcessEvent):
    """
    A minimal example of how to handle events.
    """
    def process_default(self, event):
        event_handled = False

        if event.mask & pyinotify.EventsCodes.OP_FLAGS['IN_OPEN']:
            print("%s opened" % event.pathname)
            event_handled = True
        if event.mask & pyinotify.EventsCodes.OP_FLAGS['IN_CLOSE_WRITE'] or \
            event.mask & pyinotify.EventsCodes.OP_FLAGS['IN_CLOSE_NOWRITE']:
                print("%s closed" % event.pathname)
                event_handled = True
        if event.mask & pyinotify.EventsCodes.OP_FLAGS['IN_CREATE']:
            print("%s was created" % event.pathname)
            event_handled = True
        if event.mask & pyinotify.EventsCodes.OP_FLAGS['IN_DELETE']:
            print("%s was deleted" % event.pathname)
            event_handled = True
        if event.mask & pyinotify.EventsCodes.OP_FLAGS['IN_MODIFY']:
            print("%s was modified" % event.pathname)
            event_handled = True
        if event.mask & pyinotify.EventsCodes.OP_FLAGS['IN_MOVED_FROM']:
            print("%s moved" % event.pathname)
            event_handled = True

        if event_handled:
            print("")
            can_finish = True
        else:
            print("Unhandled event %s on %s" % (event.maskname, event.pathname))
            print("")

def handle_read_callback(notifier):
    """
    Just stop receiving IO read events after the first
    iteration (unrealistic example).
    """
    print('handle_read callback')
    notifier.loop.stop()


wm = pyinotify.WatchManager()

try:
    loop = asyncio.get_running_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

notifier = pyinotify.AsyncioNotifier(wm, loop,
                                     callback=handle_read_callback,
                                     default_proc_fun=HandleEvents())
wm.add_watch('/tmp', pyinotify.ALL_EVENTS)
loop.run_forever()
notifier.stop()
