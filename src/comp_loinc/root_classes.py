import urllib.parse

from comp_loinc.datamodel import Entity, LoincTermClass
from comp_loinc.module import Module
from comp_loinc.comploinc_schema import ComploincNodeType
from loinclib import LoincNodeType, LoinclibGraph
from loinclib.loinc_schema import LoincClassProps

tree_root = f"{ComploincNodeType.root_node.value.id_prefix}:GroupTrees"
group_root = f"{ComploincNodeType.root_node.value.id_prefix}:Groups"
_groups_all = f"{ComploincNodeType.root_node.value.id_prefix}:GroupsAll"

loinc_parts = "part/LoincPart"
loinc_parts_tree = "part/LoincPartTree"
loinc_parts_tree_small = "part/LoincPartTreeSmall"
loinc_parts_tree_medium = "part/LoincPartTreeMedium"
loinc_parts_dangling = "part/LoincPartDangling"
loinc_parts_type = "part/LoincPartType"

loinc_parts_no_type = "part/LoincPartNoType"


def group_tree_root(entity: Entity, module: Module):
  root = module.getsert_entity(tree_root, Entity)
  entity.sub_class_of.append(root.id)


def groups_named(grouping_name: str, module: Module) -> Entity:
  group_named_entity = module.getsert_entity(
      f"{ComploincNodeType.root_node.value.id_prefix}:{urllib.parse.quote(grouping_name)}", Entity)
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


def get_parts() -> Entity:
  entity = Entity(id=f"{ComploincNodeType.comploinc.value.id_prefix}:{loinc_parts}")
  return entity


def get_parts_tree() -> Entity:
  entity = Entity(id=f"{ComploincNodeType.comploinc.value.id_prefix}:{loinc_parts_tree}")
  return entity


def get_parts_tree_small() -> Entity:
  entity = Entity(id=f"{ComploincNodeType.comploinc.value.id_prefix}:{loinc_parts_tree_small}")
  return entity


def get_parts_tree_medium() -> Entity:
  entity = Entity(id=f"{ComploincNodeType.comploinc.value.id_prefix}:{loinc_parts_tree_medium}")
  return entity


def get_parts_dangling() -> Entity:
  entity = Entity(id=f"{ComploincNodeType.comploinc.value.id_prefix}:{loinc_parts_dangling}")
  return entity


def get_parts_type() -> Entity:
  entity = Entity(id=f"{ComploincNodeType.comploinc.value.id_prefix}:{loinc_parts_type}")
  return entity


def get_part_no_type() -> Entity:
  return Entity(id=f"{ComploincNodeType.comploinc.value.id_prefix}:{loinc_parts_no_type}")


def get_part_type(part_type: str, module: Module) -> Entity:
  type_root = get_parts_type()

  part_type_parts = part_type.split(".")
  parent_part_entity: Entity | None = None
  part_name = None
  for part in part_type_parts:
    if part_name is None:
      part_name = "pt " + part
    else:
      part_name += "." + part
    part_entity = module.getsert_entity(
        entity_id=f"{ComploincNodeType.comploinc.value.id_prefix}:part_type/{urllib.parse.quote(part_name)}",
        entity_class=Entity)
    part_entity.entity_label = part_name

    if parent_part_entity:
      if parent_part_entity.id not in part_entity.sub_class_of:
        part_entity.sub_class_of.append(parent_part_entity.id)
        parent_part_entity.parent_of.append(part_entity.id)
    else:
      part_entity.sub_class_of.append(type_root.id)
    parent_part_entity = part_entity

  return parent_part_entity


def get_top_term_class(module: Module) -> Entity:
  return module.getsert_entity(entity_id=f"{LoincNodeType.LoincClass.value.id_prefix}:LoincTerm", entity_class=Entity)


laboratory_id = f"{ComploincNodeType.comploinc.value.id_prefix}:termclasstype/{urllib.parse.quote('ltct Laboratory')}"
clinical_id = f"{ComploincNodeType.comploinc.value.id_prefix}:termclasstype/{urllib.parse.quote('ltct Clinical')}"
claim_id = f"{ComploincNodeType.comploinc.value.id_prefix}:termclasstype/{urllib.parse.quote('ltct Claims_attachments')}"
survey_id = f"{ComploincNodeType.comploinc.value.id_prefix}:termclasstype/{urllib.parse.quote('ltct Surveys')}"


def get_term_class_type(class_type: str, module: Module) -> Entity:
  entity = module.get_entity(entity_id=laboratory_id, entity_class=Entity)
  if entity is None:
    entity = module.getsert_entity(laboratory_id, entity_class=Entity)
    entity.entity_label = 'ltct Laboratory'
    entity = module.getsert_entity(clinical_id, entity_class=Entity)
    entity.entity_label = 'ltct Clinical'
    entity =module.getsert_entity(claim_id, entity_class=Entity)
    entity.entity_label = 'ltct Claims_attachments'
    entity = module.getsert_entity(survey_id, entity_class=Entity)
    entity.entity_label = 'ltct Surveys'

  match class_type:  # todo: Possibly throw error if class_type is not a recognized case
    case "1":
      class_type_entity = module.getsert_entity(entity_id=laboratory_id, entity_class=Entity)
    case "2":
      class_type_entity = module.getsert_entity(entity_id=clinical_id, entity_class=Entity)
    case "3":
      class_type_entity = module.getsert_entity(entity_id=claim_id, entity_class=Entity)
    case "4":
      class_type_entity = module.getsert_entity(entity_id=survey_id, entity_class=Entity)

  return class_type_entity


def get_term_class(term_class: str, module: Module, class_type_entity: Entity, graph: LoinclibGraph) -> Entity:
  term_class_parts = term_class.split(".")
  parent_class_entity: LoincTermClass | None = None
  part_name = None
  for part in term_class_parts:
    if part_name is None:
      part_name = "ltc " + part
    else:
      part_name += "." + part
    class_entity = module.getsert_entity(
      entity_id=f"{ComploincNodeType.comploinc.value.id_prefix}:termclass/{urllib.parse.quote(part_name)}",
      entity_class=LoincTermClass)
    class_entity.entity_label = part_name

    if parent_class_entity:
      if parent_class_entity.id not in class_entity.sub_class_of:
        class_entity.sub_class_of.append(parent_class_entity.id)
    else:
      class_entity.sub_class_of.append(class_type_entity.id)

    parent_class_entity = class_entity

  class_node = graph.get_node_by_code(type_=LoincNodeType.LoincClass, code=term_class)
  if class_node is None:
    print("debug")
  class_title = class_node.get_property(LoincClassProps.title)
  class_part_number = class_node.get_property(LoincClassProps.part_number)

  parent_class_entity.class_abbreviation = term_class
  parent_class_entity.class_title = class_title
  parent_class_entity.class_part = class_part_number

  return parent_class_entity
