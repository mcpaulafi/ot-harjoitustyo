import unittest
from maksukortti import Maksukortti

class TestMaksukortti(unittest.TestCase):
    def setUp(self):
        self.kortti = Maksukortti(1000)

    def test_konstruktori_asettaa_saldon_oikein(self):
        self.assertEqual(str(self.kortti), "Kortilla on rahaa 10.00 euroa")


    def test_syo_edullisesti_vahentaa_saldoa_oikein(self):
        self.kortti.syo_edullisesti()

        self.assertEqual(self.kortti.saldo_euroina(), 7.5)

    def test_syo_maukkaasti_vahentaa_saldoa_oikein(self):
        self.kortti.syo_maukkaasti()

        self.assertEqual(self.kortti.saldo_euroina(), 6.0)

    def test_syo_maukkaasti_ei_vie_saldoa_negatiiviseksi(self):
        self.kortti = Maksukortti(200)
        self.kortti.syo_maukkaasti()

        self.assertEqual(self.kortti.saldo_euroina(), 2.0)

    def test_syo_edullisesti_ei_vie_saldoa_negatiiviseksi(self):
        self.kortti = Maksukortti(200)
        self.kortti.syo_edullisesti()

        self.assertEqual(self.kortti.saldo_euroina(), 2.0)

    def test_kortille_voi_ladata_rahaa(self):
        self.kortti.lataa_rahaa(2500)

        self.assertEqual(self.kortti.saldo_euroina(), 35.0)

    def test_kortin_saldo_ei_ylita_maksimiarvoa(self):
        self.kortti.lataa_rahaa(20000)

        self.assertEqual(self.kortti.saldo_euroina(), 150.0)

    def test_kortille_negatiivinen_lataus_ei_muuta_saldoa(self):
        self.kortti.lataa_rahaa(-22)

        self.assertEqual(self.kortti.saldo_euroina(), 10.0)


    def test_syo_edullisesti_kun_kortin_saldo_riittaa(self):
        self.kortti = Maksukortti(249)
        self.kortti.syo_edullisesti()

        self.assertEqual(self.kortti.saldo_euroina(), 2.49)

    def test_syo_maukkaasti_kun_kortin_saldo_riittaa(self):
        self.kortti = Maksukortti(399)
        self.kortti.syo_maukkaasti()

        self.assertEqual(self.kortti.saldo_euroina(), 3.99)
