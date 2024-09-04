from pathlib import Path

import yaml


class Configuration:
  def __init__(self, home_path: Path = Path.cwd(), config_file: Path = 'comploinc_config.yaml'):

    self.home_path = home_path
    self.config_path = home_path / config_file

    self.config = None
    if self.config_path.exists():
      with open(self.config_path, 'r') as f:
        self.config = yaml.safe_load(f)

    self.fast_run = False
    self.output = self.home_path / 'output'

  def get_loinc_release_path(self):
    try:
      default = self.config['loinc']['release']['default']
      path = self.config['loinc']['release'][default]['path']
    except KeyError as e:
      return self.home_path / 'loinc_release'
    return self.home_path / path


  def get_trees_path(self) -> Path:
    default = self.config['loinc_tree']['release']['default']
    path = self.config['loinc_tree']['release'][default]['tree_path']
    return self.home_path / path


  def get_snomed_relations_path(self) -> Path:
    release_version = self.config['snomed']['release']['default']
    relationship_path = self.config['snomed']['release'][release_version]['files']['relationship']
    return (self.home_path / relationship_path).absolute()


  def get_snomed_description_path(self) -> Path:
    default = self.config['snomed']['release']['default']
    path = self.config['snomed']['release'][default]['files']['description']
    return (self.home_path / path).absolute()

  def get_loinc_snomed_description_path(self) -> Path:
    default = self.config['loinc_snomed']['release']['default']
    path = self.config['loinc_snomed']['release'][default]['files']['description']
    return self.home_path / path

  def get_loinc_snomed_identifier_path(self) -> Path:
    default = self.config['loinc_snomed']['release']['default']
    path = self.config['loinc_snomed']['release'][default]['files']['identifier']
    return self.home_path / path

  def get_loinc_snomed_relationship_path(self) -> Path:
    default = self.config['loinc_snomed']['release']['default']
    path = self.config['loinc_snomed']['release'][default]['files']['relationship']
    return self.home_path / path

  def get_loinc_snomed_part_mapping_path(self) -> Path:
    default = self.config['loinc_snomed']['release']['default']
    path = self.config['loinc_snomed']['release'][default]['files']['part_mapping']
    return self.home_path / path

  def get_logging_configuration(self):
    return self.config['logging']

