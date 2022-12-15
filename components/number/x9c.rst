X9C Potentiometer Number
========================

.. seo::
    :description: Instructions for setting up a X9C digital potentiometer with ESPHome.
    :image: description.svg

The ``x9c`` number platform allows you to create a number that controls an `X9C digital potentiometer <https://4donline.ihs.com/images/VipMasterIC/IC/RNCC/RNCC-S-A0010771724/RNCC-S-A0010813887-1.pdf?hkey=6D3A4C79FDBF58556ACFDE234799DDF0>`__.

.. figure:: images/x9c.jpg
    :align: center
    :width: 70.0%

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
