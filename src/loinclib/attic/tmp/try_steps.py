import  comp_loinc as cl
import  typing as t
import  loinclib as ll
from loinclib import LoincLoader, GeneralEdgeType
from loinclib.loinc_tree_loader import LoincTreeLoader


class TryBuilders:
  def __init__(
      self,
      config: ll.Configuration,
  ):
    self.config = config
    self.runtime: t.Optional[cl.Runtime] = None

  def setup_builder_cli(self, builder):
    builder.cli.command(
        "try-group-parts",
        help="Specify the LOINC properties to use for grouping", hidden=True
    )(self.try_group_parts)

  def try_group_parts(self):
    loinc_loader = LoincLoader(configuration=self.config,graph=self.runtime.graph)
    loinc_loader.load_accessory_files__part_file__part_csv()

    loinc_tree_loader = LoincTreeLoader(config=self.config, graph=self.runtime.graph)
    loinc_tree_loader.load_all_trees()

    node = self.runtime.graph.get_node_by_id(node_id="loinc:LP34869-5")

    outs = list(node.get_out_edges(GeneralEdgeType.has_parent))
    ins = list(node.get_in_edges(GeneralEdgeType.has_parent))

    print('=outs=')
    print(outs)


    print('=ins=')
    print(ins)
