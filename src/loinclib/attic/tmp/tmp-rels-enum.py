from loinclib.enums import RelationTypes

print(RelationTypes.N1)
print(RelationTypes.N1.rel_group)
print(RelationTypes.N1.rel_name)
print(RelationTypes.N1.rel_uri)
print(RelationTypes.N1.name)
print(RelationTypes.N1.value)

for r in RelationTypes:
    print(r)
    print(r.rel_name)
