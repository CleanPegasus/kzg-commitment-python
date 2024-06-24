# KZG Commitment

This is a simple implementation of KZG Commitment

**KZG Commitment** is a commitment scheme that allows you to commit to a polynomial and later prove that a value is the evaluation of the polynomial at a specific point.

**This code is not audited and purely for research and education purposes only.**
**DO NOT USE IT IN PRODUCTION ENVIRONMENT**

[KZG Commitment Paper](https://www.iacr.org/archive/asiacrypt2010/6477178/6477178.pdf)
[Dankrad Feist's blog on KZG Commitment](https://dankradfeist.de/ethereum/2020/06/16/kate-polynomial-commitments.html)

### Features 
- **Galois Field Initialization**: Initializes a Galois Field with the BLS12-381 curve order.
- **Lagrange Polynomial Interpolation**: Interpolates a set of points to a polynomial in the Galois Field.
- **Trusted Setup Generation**: Generates a trusted setup for cryptographic operations.
- **Polynomial Evaluation**: Evaluates polynomials at given points using the trusted setup.
- **Zero-Knowledge Proof Generation**: Generates a zero-knowledge proof for a given polynomial and set of points.
- **Proof Verification**: Verifies the validity of a zero-knowledge proof.

### Requirements

To run this script, you need Python 3.6 or later and the following packages:

- `galois`
- `py_ecc`

You can install these packages using pip:

```bash
pip install -r requirements.txt
```

### Usage

1. Ensure you have Python 3.6 or later installed on your system.
2. Install the required packages using pip.
3. Run the script using Python:

```bash
python src/main.py
```
The script will perform the following operations:

- Initialize a Galois Field with the BLS12-381 curve order.
- Generate a trusted setup for cryptographic operations.
- Interpolate a vector to a polynomial in the Galois Field.
- Generate and verify a zero-knowledge proof for a set of points on the polynomial.

### Disclaimer
This code is not audited and is provided for research and education purposes only. Do not use it in a production environment.