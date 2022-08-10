
# Class: TimeClass




URI: [https://loinc.org/grouping_classes/TimeClass](https://loinc.org/grouping_classes/TimeClass)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[TimeClass]<subClassOf%201..*-%20[TimeClass&#124;partType(i):string%20%3F;id(i):uriorcurie;label(i):string%20%3F;description(i):string%20%3F],[LoincCodeClass]-%20has_time%200..1>[TimeClass],[PartClass]^-[TimeClass],[PartClass],[LoincCodeClass])](https://yuml.me/diagram/nofunky;dir:TB/class/[TimeClass]<subClassOf%201..*-%20[TimeClass&#124;partType(i):string%20%3F;id(i):uriorcurie;label(i):string%20%3F;description(i):string%20%3F],[LoincCodeClass]-%20has_time%200..1>[TimeClass],[PartClass]^-[TimeClass],[PartClass],[LoincCodeClass])

## Parents

 *  is_a: [PartClass](PartClass.md)

## Referenced by Class

 *  **[TimeClass](TimeClass.md)** *[TimeClass➞subClassOf](TimeClass_subClassOf.md)*  <sub>1..\*</sub>  **[TimeClass](TimeClass.md)**
 *  **None** *[has_time](has_time.md)*  <sub>0..1</sub>  **[TimeClass](TimeClass.md)**

## Attributes


### Own

 * [TimeClass➞subClassOf](TimeClass_subClassOf.md)  <sub>1..\*</sub>
     * Range: [TimeClass](TimeClass.md)

### Inherited from PartClass:

 * [id](id.md)  <sub>1..1</sub>
     * Range: [Uriorcurie](types/Uriorcurie.md)
 * [label](label.md)  <sub>0..1</sub>
     * Range: [String](types/String.md)
 * [description](description.md)  <sub>0..1</sub>
     * Range: [String](types/String.md)
 * [partType](partType.md)  <sub>0..1</sub>
     * Range: [String](types/String.md)
