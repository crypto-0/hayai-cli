import unittest
from hayai_cli.provider_parsers.extractors.utilities.decrypt import decrypt

class TestDescrypt(unittest.TestCase):

    #test to make usre that an encrypted string is being decrypted correctly
    def test_decrypt(self):
        passphrase = "9471ed28e25356e09f40091c4de1a0bf"
        encrypted = "U2FsdGVkX198MhMhv+Zj9hJBH1VMLOU8a9kJlir5ex4mM/T2mYPy+ClGWgo2gLoVsf0BKip1tI6pG6Ln4fLb3Fs2nQQYJllWXUc1Ow2U5hIEOiSR/1+fnb6iTcf2f45MJSC3D1swWvtfDeO1W6JkQ9MfuTFT1qMy2Ik3O3a/Zk+OOQdckm358VXw48voE3FwBLy4LXqZfzadyYSZY2VVDTEWWhOamv23oIqC9U3ldxI6a8xpxNNR9oDIZ6hqBebrs1QyqXk8i/EwinQYeonPGRcBGPX5O8FYZz8jox4cd9lOUdk7GTU/lofOUo58u7/mf1N/nm0lPdFKr1Dh2xFO8iTdAhq/iBW6NoN4/5DAUIFgIA7Ci2msqYs8ptQTVo0x4iUzEdrhixqbSC8mP2aUtLWAWP/kQJqfjWIhnuT6tozBqQ+HDJ0ovLWst5lOrSdNvrC7dmr+u5TeNATQJPKUb3fhF00fXEgbV4kWOX2FKuM="
        decypted = '[{"file":"https://t-ca-2.24hoursuptodatecdn.net/_v9/94d260b0390bf2844191b55b87e13c5b88d2ecacbb0a1847e5c2ae6f19bc60bbed128938bbae1307b419634d5ae5a528e4f392f43cd51d553f6c6b93bb99383aee07d6b5bfe0f3fe219913557b1c186fb295c81e7b4e803e6b75dbb321f8275ac934292acccfe54a5a4778ac1d72db0f7cc04990a8728641908c14763e977762/playlist.m3u8","type":"hls"}]'

        result = decrypt(encrypted=encrypted,passphrase=passphrase)
        self.assertEqual(result,decypted)

