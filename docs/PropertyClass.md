
# Class: PropertyClass




URI: [https://loinc.org/grouping_classes/PropertyClass](https://loinc.org/grouping_classes/PropertyClass)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[PropertyClass]<subClassOf%201..*-%20[PropertyClass&#124;partType(i):string%20%3F;id(i):uriorcurie;label(i):string%20%3F;description(i):string%20%3F],[LoincCodeClass]-%20has_property%200..1>[PropertyClass],[PartClass]^-[PropertyClass],[PartClass],[LoincCodeClass])](https://yuml.me/diagram/nofunky;dir:TB/class/[PropertyClass]<subClassOf%201..*-%20[PropertyClass&#124;partType(i):string%20%3F;id(i):uriorcurie;label(i):string%20%3F;description(i):string%20%3F],[LoincCodeClass]-%20has_property%200..1>[PropertyClass],[PartClass]^-[PropertyClass],[PartClass],[LoincCodeClass])

## Parents

 *  is_a: [PartClass](PartClass.md)

## Referenced by Class

 *  **[PropertyClass](PropertyClass.md)** *[PropertyClass➞subClassOf](PropertyClass_subClassOf.md)*  <sub>1..\*</sub>  **[PropertyClass](PropertyClass.md)**
 *  **None** *[has_property](has_property.md)*  <sub>0..1</sub>  **[PropertyClass](PropertyClass.md)**

## Attributes


### Own

 * [PropertyClass➞subClassOf](PropertyClass_subClassOf.md)  <sub>1..\*</sub>
     * Range: [PropertyClass](PropertyClass.md)

### Inherited from PartClass:

 * [id](id.md)  <sub>1..1</sub>
     * Range: [Uriorcurie](types/Uriorcurie.md)
 * [label](label.md)  <sub>0..1</sub>
     * Range: [String](types/String.md)
 * [description](description.md)  <sub>0..1</sub>
     * Range: [String](types/String.md)
 * [partType](partType.md)  <sub>0..1</sub>
     * Range: [String](types/String.md)
