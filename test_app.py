import unittest

from app import app


class EnviosAPITests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_lista_todas_las_tarifas(self):
        data = self.client.get('/api/v2/envios/tarifas').get_json()
        self.assertEqual(data['moneda'], 'COP')
        self.assertGreater(len(data['tarifas']), 1)

    def test_cotiza_ciudad_sin_importar_tildes_ni_mayusculas(self):
        response = self.client.get('/api/v2/envios/tarifas?ciudad=bogota')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['tarifas'][0]['ciudad'], 'Bogotá')

    def test_ciudad_sin_cobertura_devuelve_404(self):
        response = self.client.get('/api/v2/envios/tarifas?ciudad=Narnia')
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', response.get_json())


if __name__ == '__main__':
    unittest.main()
