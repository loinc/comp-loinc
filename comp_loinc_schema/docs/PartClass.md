
# Class: PartClass




URI: [https://loinc.org/code/PartClass](https://loinc.org/code/PartClass)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[Thing],[SystemClass],[PartClass]<subClassOf%201..*-%20[PartClass&#124;id(i):uriorcurie;label(i):string%20%3F;description(i):string%20%3F],[PartClass]^-[SystemClass],[PartClass]^-[ComponentClass],[Thing]^-[PartClass],[ComponentClass])](https://yuml.me/diagram/nofunky;dir:TB/class/[Thing],[SystemClass],[PartClass]<subClassOf%201..*-%20[PartClass&#124;id(i):uriorcurie;label(i):string%20%3F;description(i):string%20%3F],[PartClass]^-[SystemClass],[PartClass]^-[ComponentClass],[Thing]^-[PartClass],[ComponentClass])

## Parents

 *  is_a: [Thing](Thing.md)

## Children

 * [ComponentClass](ComponentClass.md)
 * [SystemClass](SystemClass.md)

## Referenced by Class

 *  **None** *[subClassOf](subClassOf.md)*  <sub>1..\*</sub>  **[PartClass](PartClass.md)**

## Attributes


### Own

 * [subClassOf](subClassOf.md)  <sub>1..\*</sub>
     * Range: [PartClass](PartClass.md)

### Inherited from Thing:

 * [id](id.md)  <sub>1..1</sub>
     * Range: [Uriorcurie](types/Uriorcurie.md)
 * [label](label.md)  <sub>0..1</sub>
     * Range: [String](types/String.md)
 * [description](description.md)  <sub>0..1</sub>
     * Range: [String](types/String.md)
