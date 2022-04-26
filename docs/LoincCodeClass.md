
# Class: LoincCodeClass




URI: [https://loinc.org/code/LoincCodeClass](https://loinc.org/code/LoincCodeClass)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[Thing],[SystemClass],[SystemClass]<has_system%200..1-%20[LoincCodeClass&#124;id(i):uriorcurie;label(i):string%20%3F;description(i):string%20%3F],[ComponentClass]<has_component%200..1-%20[LoincCodeClass],[Thing]^-[LoincCodeClass],[ComponentClass])](https://yuml.me/diagram/nofunky;dir:TB/class/[Thing],[SystemClass],[SystemClass]<has_system%200..1-%20[LoincCodeClass&#124;id(i):uriorcurie;label(i):string%20%3F;description(i):string%20%3F],[ComponentClass]<has_component%200..1-%20[LoincCodeClass],[Thing]^-[LoincCodeClass],[ComponentClass])

## Parents

 *  is_a: [Thing](Thing.md)

## Attributes


### Own

 * [has_component](has_component.md)  <sub>0..1</sub>
     * Range: [ComponentClass](ComponentClass.md)
 * [has_system](has_system.md)  <sub>0..1</sub>
     * Range: [SystemClass](SystemClass.md)

### Inherited from Thing:

 * [id](id.md)  <sub>1..1</sub>
     * Range: [Uriorcurie](types/Uriorcurie.md)
 * [label](label.md)  <sub>0..1</sub>
     * Range: [String](types/String.md)
 * [description](description.md)  <sub>0..1</sub>
     * Range: [String](types/String.md)
