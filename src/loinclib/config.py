import typing as t
from pathlib import Path

import yaml

LOINCLIB_DIR = Path(__file__).parent
PROJECT_DIR = LOINCLIB_DIR.parent.parent

class Configuration:
    def __init__(
        self, home_path: Path = PROJECT_DIR, config_file: Path = "comploinc_config.yaml"
    ):
        self.home_path = home_path
        self.config_path = home_path / config_file

        self.config = None
        if self.config_path.exists():
            with open(self.config_path, "r") as f:
                self.config = yaml.safe_load(f)

        self.fast_run = False
        self.output = self.home_path / "output"

    def get_loinc_release_path(self):
        try:
            default = self.config["loinc"]["release"]["default"]
            path = self.config["loinc"]["release"][default]["path"]
        except KeyError as e:
            return self.home_path / "loinc_release"
        return self.home_path / path

    def get_loinc_trees_path(self) -> Path:
        default = self.config["loinc_tree"]["release"]["default"]
        path = self.config["loinc_tree"]["release"][default]["tree_path"]
        return self.home_path / path

    def get_loinc_classes_path(self) -> t.Optional[Path]:
        try:
            default = self.config["loinc"]["release"]["default"]
            path = self.config["loinc"]["release"][default]["classes"]
            return self.home_path / path
        except KeyError as e:
            pass

    def get_snomed_relations_path(self) -> Path:
        release_version = self.config["snomed"]["release"]["default"]
        relationship_path = self.config["snomed"]["release"][release_version]["files"][
            "relationship"
        ]
        return (self.home_path / relationship_path).absolute()

    def get_snomed_description_path(self) -> Path:
        default = self.config["snomed"]["release"]["default"]
        path = self.config["snomed"]["release"][default]["files"]["description"]
        return (self.home_path / path).absolute()

    def get_loinc_snomed_description_path(self) -> Path:
        default = self.config["loinc_snomed"]["release"]["default"]
        path = self.config["loinc_snomed"]["release"][default]["files"]["description"]
        return self.home_path / path

    def get_loinc_snomed_identifier_path(self) -> Path:
        default = self.config["loinc_snomed"]["release"]["default"]
        path = self.config["loinc_snomed"]["release"][default]["files"]["identifier"]
        return self.home_path / path

    def get_loinc_snomed_relationship_path(self) -> Path:
        default = self.config["loinc_snomed"]["release"]["default"]
        path = self.config["loinc_snomed"]["release"][default]["files"]["relationship"]
        return self.home_path / path

    def get_loinc_snomed_part_mapping_path(self) -> Path:
        default = self.config["loinc_snomed"]["release"]["default"]
        path = self.config["loinc_snomed"]["release"][default]["files"]["part_mapping"]
        return self.home_path / path

    def get_curation_dir_path(self):
        try:
            return self.home_path / self.config["loinc_nlp_tree"]["curation_dir_path"]
        except KeyError:
            return None

    def get_logging_configuration(self):
        return self.config["logging"]

    def get_prop_use_pickle(self) -> Path:
      return self.home_path / self.config["prop_use"]["pickle"]
