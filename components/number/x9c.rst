X9C Potentiometer Number
========================

.. seo::
    :description: Instructions for setting up a X9C digital potentiometer with ESPHome.
    :image: description.svg

The ``x9c`` number platform allows you to create a number that controls a `X9C digital potentiometer <https://www.renesas.com/us/en/document/dst/x9c102-x9c103-x9c104-x9c503-datasheet>`__.

.. figure:: images/x9c.jpg
    :align: center
    :width: 70.0%

    X9C digital potentiometer

The X9C family of digital potentiometers are available in different resistance values.

==================== ===================== 
``X9C102``           ``1kΩ``
-------------------- ---------------------
``X9C103``           ``10kΩ``
-------------------- ---------------------
``X9C503``           ``50kΩ``
-------------------- ---------------------
``X9C104``           ``100kΩ``
==================== =====================

All chips are controlled by a three wire interface and feature 100 possible wiper positions (1 to 100).

.. code-block:: yaml

    # Example configuration entry
    number:
      - platform: x9c
        name: "X9C Potentiometer"
        cs_pin: GPIO25
        inc_pin: GPIO27
        ud_pin: GPIO26
        initial_value: 100

Configuration variables:
------------------------

- **name** (**Required**, string): The name of the potentiometer.
- **cs_pin** (**Required**, :ref:`Pin Schema <config-pin_schema>`): Chip Select pin
- **inc_pin** (**Required**, :ref:`Pin Schema <config-pin_schema>`): Increment pin
- **ud_pin** (**Required**, :ref:`Pin Schema <config-pin_schema>`): Up/Down pin
- **initial_value** (*Optional*, int): Manually specify the initial potentiometer value, between 1 and 100. Defaults to ``100``.
- All other options from :ref:`Number <config-number>`.

See Also
--------

- :doc:`/components/number/index`
- :apiref:`x9c/x9c.h`
- :ghedit:`Edit`
