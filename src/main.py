#
# This code is not audited and purely for research and education purposes
# DO NOT USE IT IN PRODUCTION ENVIRONMENT
#

import galois
from py_ecc.bls12_381 import G1, G2, G12, add, multiply, curve_order, pairing, eq, neg, Z1
import random
from functools import reduce

print("Initializing Galois Field with BLS12_318 curve order. This may take a while.")
GF = galois.GF(curve_order)
print("Galois Field Initialized")

# convert an integer to galois field
def convert_int_to_gf(num):
  if num < 0:
    return -GF(-num)
  else:
    return GF(num)

# interpolate the given points to return a galois polynomial
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
  xs = [convert_int_to_gf(i) for i in range(len(vector))]
  vector_gf = [convert_int_to_gf(x) for x in vector]
  return lagrange_interpolation_galois(xs, vector_gf)

# generate trusted setup
def generate_trusted_setup(degree):
  s = GF(random.randint(1, curve_order))
  return ([multiply(G1, int(s ** i)) for i in range(degree + 1)] , [multiply(G2, int(s ** i)) for i in range(degree + 1)])

def evaluate_at_trusted_setup(polynomial, trusted_setup):
  return reduce(add, (multiply(point, int(coeff)) for point, coeff in zip(trusted_setup, polynomial.coeffs[::-1])), Z1)

# generate a proof for a given point
def generate_proof(polynomial, points, trusted_setup_g1):
  x_s = [convert_int_to_gf(x) for x, y in points]
  y_s = [convert_int_to_gf(y) for x, y in points]
  
  points_polynomial = lagrange_interpolation_galois(x_s, y_s)
  numerator = polynomial - points_polynomial
  denominator = GF(1)
  for x in x_s:
    denominator = denominator * galois.Poly([GF(1), -x], GF)
  
  quotient, reminder = divmod(numerator, denominator)
  assert reminder == 0, "This is not a valid proof"

  return evaluate_at_trusted_setup(quotient, trusted_setup_g1)

# 
def verify_proof(commitment, points, proof, trusted_setup_g1, trusted_setup_g2):
  x_s = [convert_int_to_gf(x) for x, y in points]
  y_s = [convert_int_to_gf(y) for x, y in points]
  points_polynomial = lagrange_interpolation_galois(x_s, y_s)
  
  z = galois.Poly([1], GF)
  for x in x_s:
    z = z * galois.Poly([GF(1), -x], GF)
  z_s = evaluate_at_trusted_setup(z, trusted_setup_g2)
  lhs = pairing(z_s, proof)
  i_s = evaluate_at_trusted_setup(points_polynomial, trusted_setup_g1)
  rhs = pairing(G2, add(commitment, neg(i_s)))
  print(eq(lhs, rhs))
  assert eq(lhs, rhs), "The proof is invalid"


def main():
  vector = [10, 20, 36, 50, 90] # example vector
  polynomial = vector_to_polynomial(vector)
  trusted_setup_g1, trusted_setup_g2 = generate_trusted_setup(polynomial.degree)
  commitment = evaluate_at_trusted_setup(polynomial, trusted_setup_g1)
  points = [(0, 10), (1, 20)] # element 10 at index 0 and element 20 at index 1
  proof = generate_proof(polynomial, points, trusted_setup_g1)
  print(proof)
  
  verify_proof(commitment, points, proof, trusted_setup_g1, trusted_setup_g2)

if __name__ == '__main__':
  main()
