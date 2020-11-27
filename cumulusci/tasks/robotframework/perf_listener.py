from unittest import mock

from robot.result.model import TestCase


class PerfListener:
    ROBOT_LISTENER_API_VERSION = 3
    ROBOT_LIBRARY_SCOPE = "TEST CASE"
    TEST_ELAPSED_TIMES = {}

    def __init__(self):
        self.ROBOT_LIBRARY_LISTENER = self

    def start_test(self, data, result):
        self.test_id = result.id

    def end_test(self, data, result):
        if self.test_id in self.TEST_ELAPSED_TIMES:
            result.tags.add(("specified_elapsed_time",))
        self.test_id = None

    def set_elapsed_time(self, time_in_seconds: float):
        assert time_in_seconds
        elapsedtime_in_ms = round(time_in_seconds * 1000)
        self.TEST_ELAPSED_TIMES[self.test_id] = elapsedtime_in_ms


def patch_robot_elapsed_time():
    orig_elapsedtime = TestCase.elapsedtime

    @property
    def myelapsedtime(self):
        return PerfListener.TEST_ELAPSED_TIMES.get(self.id) or orig_elapsedtime.fget(
            self
        )

    return mock.patch.object(TestCase, "elapsedtime", myelapsedtime)
