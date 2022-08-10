
# loinc-owl-code-schema


**metamodel version:** 1.7.0

**version:** None





### Classes

 * [Thing](Thing.md)
     * [CodeByComponent](CodeByComponent.md)
     * [CodeBySystem](CodeBySystem.md)
     * [LoincCodeClass](LoincCodeClass.md)
     * [PartClass](PartClass.md)
         * [ComponentClass](ComponentClass.md)
         * [MethodClass](MethodClass.md)
         * [PropertyClass](PropertyClass.md)
         * [SystemClass](SystemClass.md)
         * [TimeClass](TimeClass.md)

### Mixins


### Slots

 * [description](description.md)
 * [has_component](has_component.md)
     * [CodeByComponent➞has_component](CodeByComponent_has_component.md)
 * [has_method](has_method.md)
 * [has_property](has_property.md)
 * [has_system](has_system.md)
     * [CodeBySystem➞has_system](CodeBySystem_has_system.md)
 * [has_time](has_time.md)
 * [id](id.md)
 * [label](label.md)
 * [partType](partType.md)
 * [subClassOf](subClassOf.md)
     * [ComponentClass➞subClassOf](ComponentClass_subClassOf.md)
     * [LoincCodeClass➞subClassOf](LoincCodeClass_subClassOf.md)
     * [MethodClass➞subClassOf](MethodClass_subClassOf.md)
     * [PropertyClass➞subClassOf](PropertyClass_subClassOf.md)
     * [SystemClass➞subClassOf](SystemClass_subClassOf.md)
     * [TimeClass➞subClassOf](TimeClass_subClassOf.md)

### Enums


### Subsets


### Types


#### Built in

 * **Bool**
 * **Decimal**
 * **ElementIdentifier**
 * **NCName**
 * **NodeIdentifier**
 * **URI**
 * **URIorCURIE**
 * **XSDDate**
 * **XSDDateTime**
 * **XSDTime**
 * **float**
 * **int**
 * **str**

#### Defined

 * [Boolean](types/Boolean.md)  (**Bool**)  - A binary (true or false) value
 * [Date](types/Date.md)  (**XSDDate**)  - a date (year, month and day) in an idealized calendar
 * [DateOrDatetime](types/DateOrDatetime.md)  (**str**)  - Either a date or a datetime
 * [Datetime](types/Datetime.md)  (**XSDDateTime**)  - The combination of a date and time
 * [Decimal](types/Decimal.md)  (**Decimal**)  - A real number with arbitrary precision that conforms to the xsd:decimal specification
 * [Double](types/Double.md)  (**float**)  - A real number that conforms to the xsd:double specification
 * [Float](types/Float.md)  (**float**)  - A real number that conforms to the xsd:float specification
 * [Integer](types/Integer.md)  (**int**)  - An integer
 * [Ncname](types/Ncname.md)  (**NCName**)  - Prefix part of CURIE
 * [Nodeidentifier](types/Nodeidentifier.md)  (**NodeIdentifier**)  - A URI, CURIE or BNODE that represents a node in a model.
 * [Objectidentifier](types/Objectidentifier.md)  (**ElementIdentifier**)  - A URI or CURIE that represents an object in the model.
 * [String](types/String.md)  (**str**)  - A character string
 * [Time](types/Time.md)  (**XSDTime**)  - A time object represents a (local) time of day, independent of any particular day
 * [Uri](types/Uri.md)  (**URI**)  - a complete URI
 * [Uriorcurie](types/Uriorcurie.md)  (**URIorCURIE**)  - a URI or a CURIE
