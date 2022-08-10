
# Class: LoincCodeClass




URI: [https://loinc.org/grouping_classes/LoincCodeClass](https://loinc.org/grouping_classes/LoincCodeClass)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[TimeClass],[Thing],[SystemClass],[PropertyClass],[MethodClass],[LoincCodeClass]<subClassOf%201..*-%20[LoincCodeClass&#124;id(i):uriorcurie;label(i):string%20%3F;description(i):string%20%3F],[TimeClass]<has_time%200..1-%20[LoincCodeClass],[PropertyClass]<has_property%200..1-%20[LoincCodeClass],[MethodClass]<has_method%200..1-%20[LoincCodeClass],[SystemClass]<has_system%200..1-%20[LoincCodeClass],[ComponentClass]<has_component%200..1-%20[LoincCodeClass],[Thing]^-[LoincCodeClass],[ComponentClass])](https://yuml.me/diagram/nofunky;dir:TB/class/[TimeClass],[Thing],[SystemClass],[PropertyClass],[MethodClass],[LoincCodeClass]<subClassOf%201..*-%20[LoincCodeClass&#124;id(i):uriorcurie;label(i):string%20%3F;description(i):string%20%3F],[TimeClass]<has_time%200..1-%20[LoincCodeClass],[PropertyClass]<has_property%200..1-%20[LoincCodeClass],[MethodClass]<has_method%200..1-%20[LoincCodeClass],[SystemClass]<has_system%200..1-%20[LoincCodeClass],[ComponentClass]<has_component%200..1-%20[LoincCodeClass],[Thing]^-[LoincCodeClass],[ComponentClass])

## Parents

 *  is_a: [Thing](Thing.md)

## Referenced by Class

 *  **[LoincCodeClass](LoincCodeClass.md)** *[LoincCodeClass➞subClassOf](LoincCodeClass_subClassOf.md)*  <sub>1..\*</sub>  **[LoincCodeClass](LoincCodeClass.md)**

## Attributes


### Own

 * [has_component](has_component.md)  <sub>0..1</sub>
     * Range: [ComponentClass](ComponentClass.md)
 * [has_system](has_system.md)  <sub>0..1</sub>
     * Range: [SystemClass](SystemClass.md)
 * [has_method](has_method.md)  <sub>0..1</sub>
     * Range: [MethodClass](MethodClass.md)
 * [has_property](has_property.md)  <sub>0..1</sub>
     * Range: [PropertyClass](PropertyClass.md)
 * [has_time](has_time.md)  <sub>0..1</sub>
     * Range: [TimeClass](TimeClass.md)
 * [LoincCodeClass➞subClassOf](LoincCodeClass_subClassOf.md)  <sub>1..\*</sub>
     * Range: [LoincCodeClass](LoincCodeClass.md)

### Inherited from Thing:

 * [id](id.md)  <sub>1..1</sub>
     * Range: [Uriorcurie](types/Uriorcurie.md)
 * [label](label.md)  <sub>0..1</sub>
     * Range: [String](types/String.md)
 * [description](description.md)  <sub>0..1</sub>
     * Range: [String](types/String.md)
