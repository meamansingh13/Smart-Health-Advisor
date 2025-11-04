"""Quick script to sanity-check the local alternatives feature.

Run this script from the project root to exercise `find_alternatives_local` implemented in
`main.py`. It prints sample results and exits with 0 on success.
"""
import sys
import os

# Ensure project root is on sys.path
ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, ROOT)

from main import find_alternatives_local

def main():
    tests = [
        'Metformin',
        'Paracetamol',
        'Fluconazole',
        'NonExistentMedicineXYZ'
    ]

    for t in tests:
        alts = find_alternatives_local(t)
        print(f"Query: {t}\n -> Alternatives: {alts}\n")

    print('Local alternatives check completed.')

if __name__ == '__main__':
    main()
