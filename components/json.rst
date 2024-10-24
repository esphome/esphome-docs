json Component
==============

.. seo::
    :description: Instructions for parsing and building json within ESPHome.
    :keywords: json

The ``json`` component brings json building and parsing into ESPHome functions like lambdas.

JSON is a text syntax that facilitates structured data interchange between all programming languages. JSON
is a syntax of braces, brackets, colons, and commas that is useful in many contexts, profiles, and applications.
JSON stands for JavaScript Object Notation and was inspired by the object literals of JavaScript aka
ECMAScript as defined in the ECMAScript Language Specification, Third Edition.
- https://ecma-international.org/wp-content/uploads/ECMA-404_2nd_edition_december_2017.pdf


.. code-block:: json

{
  "first_name": "John",
  "last_name": "Smith",
  "is_alive": true,
  "age": 27,
  "address": {
    "street_address": "21 2nd Street",
    "city": "New York",
    "state": "NY",
    "postal_code": "10021-3100"
  },
  "phone_numbers": [
    {
      "type": "home",
      "number": "212 555-1234"
    },
    {
      "type": "office",
      "number": "646 555-4567"
    }
  ],
  "children": [
    "Catherine",
    "Thomas",
    "Trevor"
  ],
  "spouse": null
}



Parsing JSON:
-------------

Building JSON:
--------------

