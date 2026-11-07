import pyinotify
import asyncio


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
                                     callback=handle_read_callback)
wm.add_watch('/tmp', pyinotify.ALL_EVENTS)
loop.run_forever()
notifier.stop()
