import unittest

from Libs.DataLib.requests_helper import *
from Libs.OSLib.os_helper import *


class TestRequestsHelper(unittest.TestCase):
    root_dir = os.getcwd()
    test_icon_path = os.path.join(root_dir, 'test_icon.jpeg')
    # RANDOM TEST ICON FROM INTERNET
    download_image_url = 'https://media.istockphoto.com/vectors/vector-test-icon-vector-id517420449?s=612x612'

    # @classmethod
    # def setUpClass(cls):
    #     cls.test_json = JsonManager(cls.test_json_path)

    @classmethod
    def tearDownClass(cls) -> None:
        file_delete(cls.test_icon_path)

    def test_download_file(self):
        try:
            download_file(self.download_image_url, self.test_icon_path)
            file_downloaded = file_exists(self.test_icon_path)
            self.assertTrue(file_downloaded)

        except Exception as e:
            self.fail()


if __name__ == '__main__':
    unittest.main()
