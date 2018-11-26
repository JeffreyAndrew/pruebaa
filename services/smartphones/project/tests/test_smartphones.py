import json
import unittest

from project.tests.base import BaseTestCase

from project import db
from project.api.models import Smartphone


def add_smartphone(name, brand, price, quantity, color):
    smartphone = Smartphone(
        name=name, brand=brand, price=price, quantity=quantity, color=color)
    db.session.add(smartphone)
    db.session.commit()
    return smartphone


class TestSmartphoneService(BaseTestCase):
    """Tests para el servicio Smartphones."""

    def test_ping(self):
        """Nos aseguramos que la ruta localhost:5001/smartphones/ping esta funcionando
        correctamente."""
        response = self.client.get('/smartphones/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!', data['mensaje'])
        self.assertIn('satisfactorio', data['estado'])

    def test_add_smartphone(self):
        """ Asegurando de que se pueda agregar un nuevo Smartphone a la base de
        datos."""
        with self.client:
            response = self.client.post(
                '/smartphones',
                data=json.dumps({
                    'name': 'Redmi5',
                    'brand': 'Xiaomi',
                    'price': '1200',
                    'quantity': '20',
                    'color': 'black'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn(
                'Xiaomi',
                data['mensaje']
                )
            self.assertIn('satisfactorio', data['estado'])

    def test_add_smartphone_invalid_json(self):
        """Asegurando de que se arroje un error si el objeto json esta
        vacio."""
        with self.client:
            response = self.client.post(
                '/smartphones',
                data=json.dumps({}),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Datos no validos.', data['mensaje'])
            self.assertIn('falló', data['estado'])

    def test_add_smartphone_invalid_json_keys(self):
        """
        Asegurando de que se produce un error si el objeto JSON no tiene
        un key de nombre de usuario.
        """
        with self.client:
            response = self.client.post(
                '/smartphones',
                data=json.dumps({'brand': 'prueba02'}),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Datos no validos.', data['mensaje'])
            self.assertIn('falló', data['estado'])

    def test_add_user_duplicate_smartphone(self):
        """Asegurando de que se produce un error si el correo electronico ya
        existe."""
        with self.client:
            self.client.post(
                '/smartphones',
                data=json.dumps({
                    'name': 'Prueba01',
                    'brand': 'marca01'
                }),
                content_type='application/json',
            )
            response = self.client.post(
                'smartphones',
                data=json.dumps({
                    'name': 'Prueba01',
                    'brand': 'marca01'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn(
                'Datos no validos', data['mensaje'])
            self.assertIn('falló', data['estado'])

    def test_single_smartphone(self):
        """Asegurando de que el smartphone individual se comporte
        correctamente."""
        smartphone = add_smartphone('Moto-G', 'Motorola', '100', '10', 'red')
        with self.client:
            response = self.client.get(
                f'/smartphones/{smartphone.idSmartphone}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('Moto-G', data['data']['name'])
            self.assertIn('Motorola', data['data']['brand'])
            self.assertIn('100', data['data']['price'])
            self.assertIn('10', data['data']['quantity'])
            self.assertIn('red', data['data']['color'])
            self.assertIn('satisfactorio', data['estado'])

    def test_single_user_no_id(self):
        """Asegurando de que se lanze un error si no se proporciona un id."""
        with self.client:
            response = self.client.get('/smartphones/blah')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('El smartphone no existe', data['mensaje'])
            self.assertIn('falló', data['estado'])

    def test_single_smartphone_incorrect_id(self):
        """Asegurando de que se lanze un error si el id no existe."""
        with self.client:
            response = self.client.get('/smartphones/999')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('El smartphone no existe', data['mensaje'])
            self.assertIn('falló', data['estado'])

    def test_all_smartphones(self):
        """Asegurarse de que todos los usuarios se comporte correctamente."""
        add_smartphone('nam1', 'brd1', '12', 'brd1', '12')
        add_smartphone('nam2', 'brd2', '13', 'brd2', '13')
        with self.client:
            response = self.client.get('/smartphones')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['smartphones']), 2)
            self.assertIn('nam1', data['data']['smartphones'][0]['name'])
            self.assertIn('brd1', data['data']['smartphones'][0]['brand'])
            self.assertIn('nam2', data['data']['smartphones'][1]['name'])
            self.assertIn('brd2', data['data']['smartphones'][1]['brand'])
            self.assertIn('satisfactorio', data['estado'])

    def test_main_no_smartphones(self):
        """Ensure the main route behaves correctly when no smartphones have been
        added to the database."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'All Smartphones', response.data)
#       self.assertIn(b'<p>No smartphones!</p>', response.data)

    def test_main_with_smartphones(self):
        """Ensure the main route behaves correctly when smartphones have been
        added to the database."""
        add_smartphone('nam1', 'brd1', '12', 'brd1', '12')
        add_smartphone('nam2', 'brd2', '13', 'brd2', '13')
        with self.client:
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'List Smartphones', response.data)
#           self.assertNotIn(b'<p>No smartphones!</p>', response.data)
            self.assertIn(b'nam1', response.data)
            self.assertIn(b'nam2', response.data)

    def test_main_add_smartphone(self):
        """Ensure a new user can be added to the database."""
        with self.client:
            response = self.client.post(
                '/',
                data=dict(
                    name='Prueba01', brand="marca01", price='100',
                    quantity='8', color='pink'),
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'All Smartphones', response.data)
            self.assertNotIn(b'<p>No smartphones!</p>', response.data)
            self.assertIn(b'Prueba01', response.data)


if __name__ == '__main__':
    unittest.main()
