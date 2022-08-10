
# Class: SystemClass




URI: [https://loinc.org/grouping_classes/SystemClass](https://loinc.org/grouping_classes/SystemClass)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[SystemClass]<subClassOf%201..*-%20[SystemClass&#124;partType(i):string%20%3F;id(i):uriorcurie;label(i):string%20%3F;description(i):string%20%3F],[CodeBySystem]-%20has_system%200..1>[SystemClass],[CodeBySystem]-%20has_system(i)%200..1>[SystemClass],[LoincCodeClass]-%20has_system%200..1>[SystemClass],[PartClass]^-[SystemClass],[PartClass],[LoincCodeClass],[CodeBySystem])](https://yuml.me/diagram/nofunky;dir:TB/class/[SystemClass]<subClassOf%201..*-%20[SystemClass&#124;partType(i):string%20%3F;id(i):uriorcurie;label(i):string%20%3F;description(i):string%20%3F],[CodeBySystem]-%20has_system%200..1>[SystemClass],[CodeBySystem]-%20has_system(i)%200..1>[SystemClass],[LoincCodeClass]-%20has_system%200..1>[SystemClass],[PartClass]^-[SystemClass],[PartClass],[LoincCodeClass],[CodeBySystem])

## Parents

 *  is_a: [PartClass](PartClass.md)

## Referenced by Class

 *  **[CodeBySystem](CodeBySystem.md)** *[CodeBySystem➞has_system](CodeBySystem_has_system.md)*  <sub>0..1</sub>  **[SystemClass](SystemClass.md)**
 *  **[SystemClass](SystemClass.md)** *[SystemClass➞subClassOf](SystemClass_subClassOf.md)*  <sub>1..\*</sub>  **[SystemClass](SystemClass.md)**
 *  **None** *[has_system](has_system.md)*  <sub>0..1</sub>  **[SystemClass](SystemClass.md)**

## Attributes


### Own

 * [SystemClass➞subClassOf](SystemClass_subClassOf.md)  <sub>1..\*</sub>
     * Range: [SystemClass](SystemClass.md)

### Inherited from PartClass:

 * [id](id.md)  <sub>1..1</sub>
     * Range: [Uriorcurie](types/Uriorcurie.md)
 * [label](label.md)  <sub>0..1</sub>
     * Range: [String](types/String.md)
 * [description](description.md)  <sub>0..1</sub>
     * Range: [String](types/String.md)
 * [partType](partType.md)  <sub>0..1</sub>
     * Range: [String](types/String.md)
