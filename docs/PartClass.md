
# Class: PartClass




URI: [https://loinc.org/grouping_classes/PartClass](https://loinc.org/grouping_classes/PartClass)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[TimeClass],[Thing],[SystemClass],[PropertyClass],[Thing]<subClassOf%201..*-%20[PartClass&#124;partType:string%20%3F;id(i):uriorcurie;label(i):string%20%3F;description(i):string%20%3F],[PartClass]^-[TimeClass],[PartClass]^-[SystemClass],[PartClass]^-[PropertyClass],[PartClass]^-[MethodClass],[PartClass]^-[ComponentClass],[Thing]^-[PartClass],[MethodClass],[ComponentClass])](https://yuml.me/diagram/nofunky;dir:TB/class/[TimeClass],[Thing],[SystemClass],[PropertyClass],[Thing]<subClassOf%201..*-%20[PartClass&#124;partType:string%20%3F;id(i):uriorcurie;label(i):string%20%3F;description(i):string%20%3F],[PartClass]^-[TimeClass],[PartClass]^-[SystemClass],[PartClass]^-[PropertyClass],[PartClass]^-[MethodClass],[PartClass]^-[ComponentClass],[Thing]^-[PartClass],[MethodClass],[ComponentClass])

## Parents

 *  is_a: [Thing](Thing.md)

## Children

 * [ComponentClass](ComponentClass.md)
 * [MethodClass](MethodClass.md)
 * [PropertyClass](PropertyClass.md)
 * [SystemClass](SystemClass.md)
 * [TimeClass](TimeClass.md)

## Referenced by Class


## Attributes


### Own

 * [subClassOf](subClassOf.md)  <sub>1..\*</sub>
     * Range: [Thing](Thing.md)
 * [partType](partType.md)  <sub>0..1</sub>
     * Range: [String](types/String.md)

### Inherited from Thing:

 * [id](id.md)  <sub>1..1</sub>
     * Range: [Uriorcurie](types/Uriorcurie.md)
 * [label](label.md)  <sub>0..1</sub>
     * Range: [String](types/String.md)
 * [description](description.md)  <sub>0..1</sub>
     * Range: [String](types/String.md)
