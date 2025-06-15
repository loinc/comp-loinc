"""Analyze LOINC groups to determine how deep they are

RESULTS:
Everything 1 level deep. actually this means 2 because the parent groups are the first level, but those
apparently don't show in the group column

Can verify that this is correct by adding these two rows:
"LG8749-6111","LG8749-6222","temp","","Active",""
"LG8749-6","LG8749-6111","temp","","Active",""
if you do this, then you'll see that instead of depth 1, these correctly show as depth 2 and 3.
"""
from collections import Counter
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

THIS_FILE = Path(__file__)
PROJ_DIR = THIS_FILE.parent.parent.parent.parent.parent
INPATH = str(PROJ_DIR / 'loinc_release/Loinc_2.80/AccessoryFiles/GroupFile/Group.csv')

df = pd.read_csv(INPATH)
parent_child_map = {}
for _, row in df.iterrows():
    group_id = row['GroupId']
    parent_id = row['ParentGroupId']
    if pd.notna(parent_id) and parent_id != '':
        parent_child_map[group_id] = parent_id


def calculate_depth(group_id, parent_map, memo=None):
    """Calculate hierarchy depth by traversing up the parent chain"""
    if memo is None:
        memo = {}

    # If already calculated, return cached result
    if group_id in memo:
        return memo[group_id]

    # If no parent, it's at depth 0 (root level)
    if group_id not in parent_map:
        memo[group_id] = 0
        return 0

    # Recursively calculate parent's depth and add 1
    parent_id = parent_map[group_id]
    parent_depth = calculate_depth(parent_id, parent_map, memo)
    depth = parent_depth + 1
    memo[group_id] = depth
    return depth


# Calculate depths for all groups
group_depths = {}
memo = {}
for _, row in df.iterrows():
    group_id = row['GroupId']
    depth = calculate_depth(group_id, parent_child_map, memo)
    group_depths[group_id] = depth

# Print the dictionary
print("GroupID -> Depth mapping:")
for group_id, depth in group_depths.items():
    print(f"'{group_id}': {depth}")

# Count groups at each depth level
depth_counts = Counter(group_depths.values())
print(f"\nGroups per depth level:")
for depth in sorted(depth_counts.keys()):
    print(f"Depth {depth}: {depth_counts[depth]} groups")

# Create histogram
plt.figure(figsize=(10, 6))
depths = list(depth_counts.keys())
counts = list(depth_counts.values())

plt.bar(depths, counts, alpha=0.7, color='skyblue', edgecolor='black')
plt.xlabel('Hierarchy Depth')
plt.ylabel('Number of Groups')
plt.title('Distribution of Groups by Hierarchy Depth')
plt.xticks(depths)
plt.grid(axis='y', alpha=0.3)

# Add value labels on bars
for i, v in enumerate(counts):
    plt.text(depths[i], v + 0.1, str(v), ha='center', va='bottom')

plt.tight_layout()
plt.show()

# Print summary statistics
print(f"\nSummary:")
print(f"Total groups: {len(group_depths)}")
print(f"Maximum depth: {max(group_depths.values())}")
print(f"Minimum depth: {min(group_depths.values())}")
print(f"Average depth: {sum(group_depths.values()) / len(group_depths):.2f}")
print()
