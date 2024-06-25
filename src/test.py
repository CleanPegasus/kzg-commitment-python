# import unittest
import sys
import unittest
# Add the directory containing main.py to the Python path
sys.path.append('src')

from main import KZGCommitment
from py_ecc.bn128 import G1, G2, G12, add, multiply, curve_order, pairing, eq, neg, Z1
import random

class TestKZGCommitment(unittest.TestCase):
    def setUp(self):
        self.curve_order = curve_order
        self.kzg = KZGCommitment(self.curve_order)
    
    def generate_random_vector(min_value=0, max_value=1000000):
      return [random.randint(min_value, max_value) for _ in range(random.randint(0, 100))]

    def test_vector_to_polynomial(self):
        vector = self.generate_random_vector()
        polynomial = self.kzg.vector_to_polynomial(vector)
        self.assertTrue(polynomial.degree + 1 == len(vector), "Polynomial should not be None")
        random_index = random.randint(0, 100)
        self.assertTrue(polynomial(random_index) == vector[random_index])

    def test_commit_polynomial(self):
        vector = self.generate_random_vector()
        polynomial = self.kzg.vector_to_polynomial(vector)
        commitment = self.kzg.commit_polynomial(polynomial)
        self.assertIsNotNone(commitment, "Commitment should not be None")

    def test_generate_and_verify_proof(self):
        vector = self.generate_random_vector()
        polynomial = self.kzg.vector_to_polynomial(vector)
        commitment = self.kzg.commit_polynomial(polynomial)
        points = []
        for i in range(random.randint(0, 20)):
            random_index = random.randint(0, 100)
            points.append((random_index, vector[random_index]))
        proof = self.kzg.generate_proof(polynomial, points)
        self.assertIsNotNone(proof, "Proof should not be None")
        verification_result = self.kzg.verify_proof(commitment, points, proof)
        self.assertTrue(verification_result, "Proof verification should succeed")
