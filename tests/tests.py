from unittest import TestCase
from app import app
from models import db, Cupcake

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///cupcake_test"
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True

db.drop_all()
db.create_all()

test1 = {
    "flavor": "TestFlavor",
    "size": "TestSize",
    "rating": 1,
    "image": "http://test.com/cupcake.jpg"
}

test2 = {
    "flavor": "TestFlavor2",
    "size": "TestSize2",
    "rating": 2.5,
    "image": "http://test.com/cupcake2.jpg"
}

class CupcakeViews(TestCase):
    """tests views on cupcakes"""
    def setUp(self):
        """demo data"""
        Cupcake.query.delete()
        db.session.commit()

        cupcake=Cupcake(**test1)
        db.session.add(cupcake)
        db.session.commit()

        self.cupcake=cupcake
    
    def tearDown(self):
        """clean up fouled"""
        db.session.rollback()

    def test_all_cupcakes(self):
        """json for full list renders"""
        with app.test_client() as client:
            res = client.get('/api/cupcakes')
            self.assertEqual(res.status_code, 200)
            self.assertEqual(res.json, {'cupcakes': 
                [{'id': self.cupcake.id, 
                'flavor': 'TestFlavor',
                'size':'TestSize', 
                'rating':1, 
                'image':'http://test.com/cupcake.jpg'}]})

    def test_one(self):
        """json for one cupcake renders"""
        with app.test_client() as client:
            res = client.get(f"/api/cupcakes/{self.cupcake.id}")
            self.assertEqual(res.status_code, 200)
            self.assertEqual(res.json, {'cupcakes': 
                [{'id': self.cupcake.id, 
                'flavor': 'TestFlavor',
                'size':'TestSize', 
                'rating':1, 
                'image':'http://test.com/cupcake.jpg'}]})

    def test_create(self):
        """test addition of new cupcake"""
        with app.test_client() as client:
            res = client.post('/api/cupcakes', json=test2)
            self.assertEqual(res.status_code,201)
            self.assertEqual(res.json, {'cupcakes': [{
                'flavor': 'TestFlavor2',
                'size':'TestSize2', 
                'rating':2.5, 
                'image':'http://test.com/cupcake2.jpg'}]})
            self.assertEqual(Cupcake.query.count(),2)

    def test_delete(self):
        """test cupcake removal"""
        with app.test_client() as client:
            res = client.delete(f'/api/cupcakes/{self.cupcake.id}')
            self.assertEqual(res.status_code,200)

            d = res.json
            self.assertEqual(d,{'message':'deleted'})
            self.assertEqual(Cupcake.query.count(),0)

    def test_delete_404(self):
        """cannot delete cupcake @ invalid cupcake id"""
        with app.test_client() as client:
            res = client.delete(f"/api/cupcakes/1000000000")
            self.assertEqual(res.status_code,404)

    def test_patch_404(self):
        """cannot update w/ invalid cupcake id"""
        with app.test_client() as client:
            res = client.patch(f"/api/cupcakes/1000000000", json=test2)
            self.assertEqual(res.status_code,404)

    def test_get_404(self):
        """cannot retrieve data of invalid cupcake id"""
        with app.test_client() as client:
            res = client.get(f"/api/cupcakes/1000000000")
            self.assertEqual(res.status_code,404)