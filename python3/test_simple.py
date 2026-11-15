import os
import pyinotify
import tempfile
import shutil
import sys

event_holder = []
mask_holder = []


class processor(pyinotify.ProcessEvent):
    def process_default(self, event):
        event_holder.append(event)
        mask_holder.append(event.mask)


class TestPyinotifyEvents:

    @classmethod
    def setup_class(self):
        del event_holder[:]
        del mask_holder[:]
        self.watch_directory = tempfile.mkdtemp()
        self.wm = pyinotify.WatchManager()
        self.wm.add_watch(self.watch_directory, pyinotify.ALL_EVENTS)
        self.notifier = pyinotify.Notifier(self.wm, processor())

        self.is_freebsd = sys.platform.startswith('freebsd')
        self.is_linux = sys.platform.startswith('linux')

    @classmethod
    def teardown_class(self):
        shutil.rmtree(self.watch_directory)

    def _print_events(self):
        for e in event_holder:
            print(e.pathname, e.maskname)

    def _clear_events(self):
        del event_holder[:]
        del mask_holder[:]

    def _get_events(self):
        while self.notifier.read_events() > 0:
            self.notifier.process_events()

    def _check_events(self, expected):
        for i, mask in enumerate(expected):
            if self.is_linux:
                assert mask == event_holder[i].mask
            else:
                # The events may come in a different order outside of Linux.
                assert mask in mask_holder

    def test_create_event(self):
        filename = os.path.join(self.watch_directory, "tmp")
        fh = open(filename, "w")
        fh.write("")
        fh.close()

        self._clear_events()
        self._get_events()
        if self.is_linux:
            self._check_events([pyinotify.IN_CREATE,
                                pyinotify.IN_OPEN,
                                pyinotify.IN_CLOSE_WRITE])
        else:
            self._check_events([pyinotify.IN_CREATE])

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
        if self.is_linux:
            assert pyinotify.IN_MOVED_FROM == event_holder[-1].mask
        else:
            assert (pyinotify.IN_MOVED_FROM in mask_holder) or (pyinotify.IN_CREATE in mask_holder)

        self._clear_events()

        # Move file into directory
        shutil.move(filename2, filename)
        self._get_events()
        if self.is_linux:
            assert pyinotify.IN_MOVED_TO == event_holder[-1].mask
        else:
            assert (pyinotify.IN_MOVED_TO in mask_holder) or (pyinotify.IN_DELETE in mask_holder)

        self._clear_events()

        # Move file within directory
        filename3 = os.path.join(self.watch_directory, "tmp2")
        shutil.move(filename, filename3)
        self._get_events()

        if self.is_linux:
            self._check_events([pyinotify.IN_MOVED_FROM, pyinotify.IN_MOVED_TO])
        else:
            assert (pyinotify.IN_MOVED_FROM in mask_holder) or (pyinotify.IN_MOVED_TO in mask_holder)
        assert filename == event_holder[0].pathname
        if pyinotify.IN_MOVED_TO in mask_holder:
            assert filename3 == event_holder[1].pathname

    def test_modify_events(self):
        filename = os.path.join(self.watch_directory, "tmp")
        fh = open(filename, "w")
        fh.write("foo")
        fh.close()
        self._get_events()
        self._clear_events()

        fh = open(filename, "a")
        fh.write("bar")
        fh.close()

        self._get_events()
        if self.is_linux:
            self._check_events([pyinotify.IN_OPEN,
                                pyinotify.IN_MODIFY,
                                pyinotify.IN_CLOSE_WRITE])
        elif self.is_freebsd:
            self._check_events([pyinotify.IN_OPEN,
                                pyinotify.IN_CLOSE_WRITE])
        else:
            self._check_events([pyinotify.IN_MODIFY])


    def test_delete_event(self):
        filename = os.path.join(self.watch_directory, "tmp")
        fh = open(filename, "w")
        fh.write("")
        fh.close()
        self._get_events()
        self._clear_events()

        os.remove(filename)
        self._get_events()

        self._print_events()
        self._check_events([pyinotify.IN_DELETE])
