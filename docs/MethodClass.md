
# Class: MethodClass




URI: [https://loinc.org/grouping_classes/MethodClass](https://loinc.org/grouping_classes/MethodClass)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[PartClass],[MethodClass]<subClassOf%201..*-%20[MethodClass&#124;partType(i):string%20%3F;id(i):uriorcurie;label(i):string%20%3F;description(i):string%20%3F],[LoincCodeClass]-%20has_method%200..1>[MethodClass],[PartClass]^-[MethodClass],[LoincCodeClass])](https://yuml.me/diagram/nofunky;dir:TB/class/[PartClass],[MethodClass]<subClassOf%201..*-%20[MethodClass&#124;partType(i):string%20%3F;id(i):uriorcurie;label(i):string%20%3F;description(i):string%20%3F],[LoincCodeClass]-%20has_method%200..1>[MethodClass],[PartClass]^-[MethodClass],[LoincCodeClass])

## Parents

 *  is_a: [PartClass](PartClass.md)

## Referenced by Class

 *  **[MethodClass](MethodClass.md)** *[MethodClass➞subClassOf](MethodClass_subClassOf.md)*  <sub>1..\*</sub>  **[MethodClass](MethodClass.md)**
 *  **None** *[has_method](has_method.md)*  <sub>0..1</sub>  **[MethodClass](MethodClass.md)**

## Attributes


### Own

 * [MethodClass➞subClassOf](MethodClass_subClassOf.md)  <sub>1..\*</sub>
     * Range: [MethodClass](MethodClass.md)

### Inherited from PartClass:

 * [id](id.md)  <sub>1..1</sub>
     * Range: [Uriorcurie](types/Uriorcurie.md)
 * [label](label.md)  <sub>0..1</sub>
     * Range: [String](types/String.md)
 * [description](description.md)  <sub>0..1</sub>
     * Range: [String](types/String.md)
 * [partType](partType.md)  <sub>0..1</sub>
     * Range: [String](types/String.md)
