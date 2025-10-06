import urllib.parse

from comp_loinc.datamodel import  Entity
from comp_loinc.module import  Module
from comp_loinc.comploinc_schema import  ComploincNodeType

tree_root = f"{ComploincNodeType.root_node.value.id_prefix}:GroupTrees"
group_root = f"{ComploincNodeType.root_node.value.id_prefix}:Groups"
_groups_all = f"{ComploincNodeType.root_node.value.id_prefix}:GroupsAll"

def group_tree_root(entity: Entity, module: Module):
  root = module.getsert_entity(tree_root, Entity)
  entity.sub_class_of.append(root.id)

def groups_named(grouping_name: str, module: Module) -> Entity:

  group_named_entity = module.getsert_entity(f"{ComploincNodeType.root_node.value.id_prefix}:{urllib.parse.quote_plus(grouping_name)}", Entity)
  group_named_entity.entity_label = grouping_name

  groups_all(group_named_entity, module)

  return group_named_entity

def groups_all(entity: Entity, module: Module) -> Entity:
  groups_all_entity = module.getsert_entity(_groups_all, Entity)

  if groups_all_entity.id not in entity.sub_class_of:
    entity.sub_class_of.append(groups_all_entity.id)
  return groups_all_entity

def group_single_root(entity: Entity, module: Module):
  root = module.getsert_entity(group_root, Entity)
  entity.sub_class_of.append(root.id)




def _add_class_to_module(entity_id: str, entity: Entity, module: Module):
  pass