from comp_loinc.datamodel import  Entity
from comp_loinc.module import  Module
from comp_loinc.comploinc_schema import  ComploincNodeType

tree_root = f"{ComploincNodeType.root_node.value.id_prefix}:GroupTrees"
group_root = f"{ComploincNodeType.root_node.value.id_prefix}:Groups"

def group_tree_root(entity: Entity, module: Module):
  root = module.getsert_entity(tree_root, Entity)
  entity.sub_class_of.append(root.id)


def group_single_root(entity: Entity, module: Module):
  root = module.getsert_entity(group_root, Entity)
  entity.sub_class_of.append(root.id)



def _add_class_to_module(entity_id: str, entity: Entity, module: Module):
  pass