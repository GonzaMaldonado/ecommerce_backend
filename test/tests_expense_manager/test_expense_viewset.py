from test.test_setup import TestSetUp
from test.factories.expense_manager.expense_factories import SupplierFactory
from apps.expense_manager.models import Supplier

from rest_framework import status

# Funciona como un debug cuando ejecuto manage.py test, se detiene donde lo puse y me deja acceder a cada
# variable que este antes de su definición
#import pdb; pdb.set_trace()

class ExpenseTestCase(TestSetUp):
    url = '/expenses/expense'
    
    def test_search_supplier(self):
        supplier = SupplierFactory().create_supplier()
        response = self.client.get(
            # La Ruta
            f'{self.url}/search_supplier/',
            # Que necesita la ruta, en este caso en params se manda ruc_or_business_name
            {
                'ruc_or_business_name': supplier.ruc
            },
            # El formato
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['ruc'], supplier.ruc)


    def test_search_supplier_error(self):
        supplier = SupplierFactory().create_supplier()
        response = self.client.get(
            f'{self.url}/search_supplier/',
            {
                'ruc_or_business_name': '123456789'
            },
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertNotEqual(supplier.ruc, '123456789')
        self.assertEqual(response.data['error'], 'No se ha encontrado un Proveedor')


    def test_new_supplier(self):
        supplier = SupplierFactory().build_supplier_JSON()
        response = self.client.post(
            f'{self.url}/new_supplier/',
            supplier,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Supplier.objects.all().count(), 1)
        self.assertEqual(response.data['supplier']['ruc'], supplier['ruc'])