import os
import pyinotify
import tempfile
import shutil

event_holder = []


class processor(pyinotify.ProcessEvent):
    def process_default(self, event):
        event_holder.append(event)


class TestPyinotifyEvents:

    @classmethod
    def setup_class(self):
        del event_holder[:]
        self.watch_directory = tempfile.mkdtemp()
        self.wm = pyinotify.WatchManager()
        self.wm.add_watch(self.watch_directory, pyinotify.ALL_EVENTS)
        self.notifier = pyinotify.Notifier(self.wm, processor())

    @classmethod
    def teardown_class(self):
        shutil.rmtree(self.watch_directory)

    def _print_events(self):
        for e in event_holder:
            print(e.pathname, e.maskname)

    def _get_events(self):
        while self.notifier.read_events() > 0:
            self.notifier.process_events()

    def _check_events(self, expected):
        for i, mask in enumerate(expected):
            assert mask == event_holder[i].mask

    def test_create_event(self):
        filename = os.path.join(self.watch_directory, "tmp")
        fh = open(filename, "w")
        fh.write("")
        fh.close()
        self._get_events()
        self._check_events([pyinotify.IN_CREATE,
                            pyinotify.IN_OPEN,
                            pyinotify.IN_CLOSE_WRITE])

    def test_move_event(self):
        filename = os.path.join(self.watch_directory, "tmp")
        second_dir = tempfile.mkdtemp()
        filename2 = os.path.join(second_dir, "tmp")

        fh = open(filename, "w")
        fh.write("")
        fh.close()

        self._get_events()

        # Move file out of directory
        shutil.move(filename, filename2)
        self._get_events()
        assert pyinotify.IN_MOVED_FROM == event_holder[-1].mask

        del event_holder[:]

        # Move file into directory
        shutil.move(filename2, filename)
        self._get_events()
        assert pyinotify.IN_MOVED_TO == event_holder[-1].mask

        del event_holder[:]

        # Move file within directory
        filename3 = os.path.join(self.watch_directory, "tmp2")
        shutil.move(filename, filename3)
        self._get_events()

        self._check_events([pyinotify.IN_MOVED_FROM, pyinotify.IN_MOVED_TO])
        assert filename == event_holder[0].pathname
        assert filename3 == event_holder[1].pathname

    def test_modify_events(self):
        filename = os.path.join(self.watch_directory, "tmp")
        fh = open(filename, "w")
        fh.write("")
        fh.close()
        self._get_events()
        del event_holder[:]

        fh = open(filename, "a")
        fh.write("foo")
        fh.close()

        self._get_events()
        self._check_events([pyinotify.IN_OPEN,
                            pyinotify.IN_MODIFY,
                            pyinotify.IN_CLOSE_WRITE])


    def test_delete_event(self):
        filename = os.path.join(self.watch_directory, "tmp")
        fh = open(filename, "w")
        fh.write("")
        fh.close()
        self._get_events()
        del event_holder[:]

        os.remove(filename)
        self._get_events()

        self._print_events()
        self._check_events([pyinotify.IN_DELETE])
