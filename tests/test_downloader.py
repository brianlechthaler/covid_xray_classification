import unittest
from covid_xray_classification.data import Downloader
from subprocess import run


class DownloaderTestCase(unittest.TestCase):
    def test_download_fashion_mnist(self):
        dl = Downloader(dataset='zalando-research/fashionmnist')
        dl.download()
        sha512sum = run(['shasum', '-a', '512', 'dataset/fashion-mnist_train.csv'],
                        capture_output=True)
        run(['rm', '-rf', 'dataset'])
        self.assertEqual(sha512sum.stdout,
                         b'5dd427e98d221d25a99bf549a571696a2aadf0a43257328189c256d69524945071efe60067cd2458dac4353cc389e83d688b0b2718cac0176a3ed67a4807d6a8  dataset/fashion-mnist_train.csv\n')


if __name__ == '__main__':
    unittest.main()
