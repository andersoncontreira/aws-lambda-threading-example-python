import unittest
import app


class AppTestCase(unittest.TestCase):
    def test_process_handler(self):
        result = app.process_handler({}, {})
        self.assertTrue(result != [])

    def test_thread_handler(self):
        result = app.thread_handler({}, {})
        self.assertTrue(result != [])


if __name__ == '__main__':
    unittest.main()
