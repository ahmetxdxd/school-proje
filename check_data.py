import sys
import os
import re

# Add current dir to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from unit01 import get_unit_1
from unit02 import get_unit_2
from unit03 import get_unit_3
from unit04 import get_unit_4
from unit05 import get_unit_5
from unit06 import get_unit_6
from unit07 import get_unit_7
from unit08 import get_unit_8
from unit09 import get_unit_9
from unit10 import get_unit_10

all_units = {
    1: get_unit_1(),
    2: get_unit_2(),
    3: get_unit_3(),
    4: get_unit_4(),
    5: get_unit_5(),
    6: get_unit_6(),
    7: get_unit_7(),
    8: get_unit_8(),
    9: get_unit_9(),
    10: get_unit_10()
}

total_count = sum(len(words) for words in all_units.values())
print(f"Total entries loaded: {total_count}")
for u, words in all_units.items():
    print(f"Unit {u}: {len(words)} entries")

# Check for empty fields or formatting issues
issues = []
for u, words in all_units.items():
    for idx, w in enumerate(words):
        if not w.get("word"):
            issues.append(f"Unit {u} entry {idx} missing word")
        if not w.get("pos"):
            issues.append(f"Unit {u} entry {w.get('word')} missing pos")
        if not w.get("definition"):
            issues.append(f"Unit {u} entry {w.get('word')} missing definition")
        if not w.get("example"):
            issues.append(f"Unit {u} entry {w.get('word')} missing example")
        if not w.get("tr"):
            issues.append(f"Unit {u} entry {w.get('word')} missing tr")

if issues:
    print(f"Found {len(issues)} issues:")
    for iss in issues[:10]:
        print(" -", iss)
else:
    print("All entries validated successfully!")
