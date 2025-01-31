import  typing as t
from comp_loinc.groups2.group import Group

class Groups:
  def __init__(self,config, module):
    self.config = config
    self.module = module
    self.initted = False

    self.groups: t.Dict[str, Group] = dict()




  def init(self):
    if self.initted:
      return
    self.initted = True

    print("INITTING GROUPER")