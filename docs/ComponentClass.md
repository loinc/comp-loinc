
# Class: ComponentClass




URI: [https://loinc.org/code/ComponentClass](https://loinc.org/code/ComponentClass)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[PartClass],[ComponentClass]<subClassOf%201..*-%20[ComponentClass&#124;id(i):uriorcurie;label(i):string%20%3F;description(i):string%20%3F],[LoincCodeClass]-%20has_component%200..1>[ComponentClass],[PartClass]^-[ComponentClass],[LoincCodeClass])](https://yuml.me/diagram/nofunky;dir:TB/class/[PartClass],[ComponentClass]<subClassOf%201..*-%20[ComponentClass&#124;id(i):uriorcurie;label(i):string%20%3F;description(i):string%20%3F],[LoincCodeClass]-%20has_component%200..1>[ComponentClass],[PartClass]^-[ComponentClass],[LoincCodeClass])

## Parents

 *  is_a: [PartClass](PartClass.md)

## Referenced by Class

 *  **[ComponentClass](ComponentClass.md)** *[ComponentClass➞subClassOf](ComponentClass_subClassOf.md)*  <sub>1..\*</sub>  **[ComponentClass](ComponentClass.md)**
 *  **None** *[has_component](has_component.md)*  <sub>0..1</sub>  **[ComponentClass](ComponentClass.md)**

## Attributes


### Own

 * [ComponentClass➞subClassOf](ComponentClass_subClassOf.md)  <sub>1..\*</sub>
     * Range: [ComponentClass](ComponentClass.md)

### Inherited from PartClass:

 * [id](id.md)  <sub>1..1</sub>
     * Range: [Uriorcurie](types/Uriorcurie.md)
 * [label](label.md)  <sub>0..1</sub>
     * Range: [String](types/String.md)
 * [description](description.md)  <sub>0..1</sub>
     * Range: [String](types/String.md)
