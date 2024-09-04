from importlib import resources

from . import schema
from .runtime import Runtime
from .cli import CompLoincCli, comploinc_cli, BuilderCli

schemas_path = resources.files(schema)
