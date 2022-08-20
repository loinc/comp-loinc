
# Class: CodeBySystem




URI: [https://loinc.org/grouping_classes/CodeBySystem](https://loinc.org/grouping_classes/CodeBySystem)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[Thing],[SystemClass],[SystemClass]<has_system%200..1-%20[CodeBySystem&#124;id(i):uriorcurie;label(i):string%20%3F;description(i):string%20%3F],[Thing]^-[CodeBySystem])](https://yuml.me/diagram/nofunky;dir:TB/class/[Thing],[SystemClass],[SystemClass]<has_system%200..1-%20[CodeBySystem&#124;id(i):uriorcurie;label(i):string%20%3F;description(i):string%20%3F],[Thing]^-[CodeBySystem])

## Parents

 *  is_a: [Thing](Thing.md)

## Referenced by Class


## Attributes


### Own

 * [CodeBySystem➞has_system](CodeBySystem_has_system.md)  <sub>0..1</sub>
     * Range: [SystemClass](SystemClass.md)

### Inherited from Thing:

 * [id](id.md)  <sub>1..1</sub>
     * Range: [Uriorcurie](types/Uriorcurie.md)
 * [label](label.md)  <sub>0..1</sub>
     * Range: [String](types/String.md)
 * [description](description.md)  <sub>0..1</sub>
     * Range: [String](types/String.md)
