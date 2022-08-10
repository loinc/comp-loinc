
# Class: Thing




URI: [https://loinc.org/grouping_classes/Thing](https://loinc.org/grouping_classes/Thing)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[PartClass]-%20subClassOf%201..*>[Thing&#124;id:uriorcurie;label:string%20%3F;description:string%20%3F],[LoincCodeClass]-%20subClassOf(i)%201..*>[Thing],[Thing]^-[PartClass],[Thing]^-[LoincCodeClass],[Thing]^-[CodeBySystem],[Thing]^-[CodeByComponent],[PartClass],[LoincCodeClass],[CodeBySystem],[CodeByComponent])](https://yuml.me/diagram/nofunky;dir:TB/class/[PartClass]-%20subClassOf%201..*>[Thing&#124;id:uriorcurie;label:string%20%3F;description:string%20%3F],[LoincCodeClass]-%20subClassOf(i)%201..*>[Thing],[Thing]^-[PartClass],[Thing]^-[LoincCodeClass],[Thing]^-[CodeBySystem],[Thing]^-[CodeByComponent],[PartClass],[LoincCodeClass],[CodeBySystem],[CodeByComponent])

## Children

 * [CodeByComponent](CodeByComponent.md)
 * [CodeBySystem](CodeBySystem.md)
 * [LoincCodeClass](LoincCodeClass.md)
 * [PartClass](PartClass.md)

## Referenced by Class

 *  **None** *[subClassOf](subClassOf.md)*  <sub>1..\*</sub>  **[Thing](Thing.md)**

## Attributes


### Own

 * [id](id.md)  <sub>1..1</sub>
     * Range: [Uriorcurie](types/Uriorcurie.md)
 * [label](label.md)  <sub>0..1</sub>
     * Range: [String](types/String.md)
 * [description](description.md)  <sub>0..1</sub>
     * Range: [String](types/String.md)

## Other properties

|  |  |  |
| --- | --- | --- |
| **Mappings:** | | owl:Class |

