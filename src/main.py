#
# This code is not audited and purely for research and education purposes
# DO NOT USE IT IN PRODUCTION ENVIRONMENT
#

import galois
from py_ecc.bn128 import G1, G2, G12, add, multiply, curve_order, pairing, eq, neg, Z1
import random
from functools import reduce
from scipy.interpolate import lagrange

print("Initializing Galois Field with BN128 curve order. This may take a while")
GF = galois.GF(curve_order)
print("Galois Field Initialized")

def lagrange_interpolation_galois(xs, ys):
  assert len(xs) == len(ys), "Length mismatch"
  length = len(xs)
  def pi(j, y):
    p_result = GF(1)
    for k in range(length):
      if k == j:
        continue
      q, _ = divmod(galois.Poly([GF(1), -xs[k]], GF), (xs[j] - xs[k]))
      p_result = p_result * q
    return y * p_result
  
  result = GF(0)
  for i in range(length):
    result = result + pi(i, ys[i])

  return result

# lagrange interpolation to convert vector to a galois polynomial
def vector_to_polynomial(vector):
  xs = [GF(i) for i in range(len(vector))]
  vector_gf = [GF(x) for x in vector]
  return lagrange_interpolation_galois(xs, vector_gf)

# generate trusted setup
def generate_trusted_setup(degree):
  s = GF(random.randint(1, curve_order))
  return ([multiply(G1, int(s ** i)) for i in range(degree + 1)] , [multiply(G2, int(s ** i)) for i in range(degree + 1)])

def evaluate_at_trusted_setup(polynomial, trusted_setup):
  return reduce(add, (multiply(point, int(coeff)) for point, coeff in zip(trusted_setup, polynomial.coeffs[::-1])), Z1)

def generate_proof(polynomial, points, trusted_setup_g1):
  x_s = [GF(x) for x, y in points]
  y_s = [GF(y) for x, y in points]
  
  points_polynomial = lagrange_interpolation_galois(x_s, y_s)
  numerator = polynomial - points_polynomial
  denominator = GF(1)
  for x in x_s:
    denominator = denominator * galois.Poly([GF(1), -x], GF)
  
  quotient, reminder = divmod(numerator, denominator)
  assert reminder == 0

  return evaluate_at_trusted_setup(quotient, trusted_setup_g1)

def verify_proof(commitment, points, proof, trusted_setup_g2, trusted_setup_g1):
  x_s = [GF(x) for x, y in points]
  y_s = [GF(y) for x, y in points]
  points_polynomial = lagrange_interpolation_galois(x_s, y_s)
  
  z = galois.Poly([1], GF)
  for x in x_s:
    z = z * galois.Poly([GF(1), -x], GF)
  z_s = evaluate_at_trusted_setup(z, trusted_setup_g2)
  lhs = pairing(z_s, proof)
  i_s = evaluate_at_trusted_setup(points_polynomial, trusted_setup_g1)
  print("i_s", i_s)
  rhs = pairing(G2, add(commitment, neg(i_s)))
  print(eq(lhs, rhs))
  assert eq(lhs, rhs), "The proof is invalid"



def main():

  trusted_setup_g1, trusted_setup_g2 = generate_trusted_setup(polynomial.degree)
  vector = [10, 20, 36, 50, 90]
  polynomial = vector_to_polynomial(vector)
  commitment = evaluate_at_trusted_setup(polynomial, trusted_setup_g1)
  points = [(0, 10), (1, 20)]
  proof = generate_proof(polynomial, points, trusted_setup_g1)
  print(proof)
  
  verify_proof(commitment, [(0, 10), (1, 20)], proof, trusted_setup_g2, trusted_setup_g1)

main()
