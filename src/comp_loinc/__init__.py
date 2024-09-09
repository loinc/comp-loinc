from importlib import resources

from . import schema, builds
from .runtime import Runtime
from .cli import CompLoincCli, comploinc_cli, BuilderCli

schemas_path = resources.files(schema)
builds_path = resources.files(builds)
