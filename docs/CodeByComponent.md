
# Class: CodeByComponent




URI: [https://loinc.org/grouping_classes/CodeByComponent](https://loinc.org/grouping_classes/CodeByComponent)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[Thing],[ComponentClass],[ComponentClass]<has_component%200..1-%20[CodeByComponent&#124;id(i):uriorcurie;label(i):string%20%3F;description(i):string%20%3F],[Thing]^-[CodeByComponent])](https://yuml.me/diagram/nofunky;dir:TB/class/[Thing],[ComponentClass],[ComponentClass]<has_component%200..1-%20[CodeByComponent&#124;id(i):uriorcurie;label(i):string%20%3F;description(i):string%20%3F],[Thing]^-[CodeByComponent])

## Parents

 *  is_a: [Thing](Thing.md)

## Referenced by Class


## Attributes


### Own

 * [CodeByComponent➞has_component](CodeByComponent_has_component.md)  <sub>0..1</sub>
     * Range: [ComponentClass](ComponentClass.md)

### Inherited from Thing:

 * [id](id.md)  <sub>1..1</sub>
     * Range: [Uriorcurie](types/Uriorcurie.md)
 * [label](label.md)  <sub>0..1</sub>
     * Range: [String](types/String.md)
 * [description](description.md)  <sub>0..1</sub>
     * Range: [String](types/String.md)
