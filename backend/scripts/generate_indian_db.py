import os
import json

# Ensure scripts directory exists
os.makedirs("backend/scripts", exist_ok=True)

# Build comprehensive Indian Plants Knowledge Base with 180+ species
generator_code = '''"""
Database Generator for 180+ Indian Plants, Crops, Spices, Fruits, Vegetables, Ayurvedic Herbs, Houseplants, and Soils
"""
import sys
import os

print("Generating comprehensive Indian Agricultural & Botanical Database...")
'''
with open("backend/scripts/generate_indian_db.py", "w", encoding="utf-8") as f:
    f.write(generator_code)
print("Stub written.")
