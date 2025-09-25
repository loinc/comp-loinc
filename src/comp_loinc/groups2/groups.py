import typing as t

from comp_loinc.groups2.group import Group
from comp_loinc.module import Module


class Groups:
  def __init__(self, module: Module):
    self.module = module
    self.initted = False

    self.groups: t.Dict[str, Group] = dict()
    self.roots: t.Dict[str, Group] = {}

  def init(self):
    if self.initted:
      return
    self.initted = True

    print("INITTING GROUPER")
