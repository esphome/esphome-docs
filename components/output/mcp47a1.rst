MCP47A1 Output
==============

.. seo::
    :description: Instructions for setting up MCP47A1 outputs on the ESP.
    :image: mcp47a1.svg

The ``mcp47a1`` output component allows to use `6bit external DAC <https://www.microchip.com/en-us/product/MCP47A1>`__
in order to have analog output(s) on any board by using I²C. Devices default address is ``0x2E``
and configurable alternative is ``0x3E``.

.. code-block:: yaml

    # Example configuration entry

    # Set a global I²C connection
    i2c:
      sda: 21
      scl: 22
      scan: true

    # Set the output with default (address: 0x2E / global I²C)
    output:
      - platform: mcp47a1
        id: dac_output

    on_...:
      then:
        - output.set_level:
            id: dac_output
            level: 100%


Configuration variables:
------------------------

- **id** (**Required**, :ref:`config-id`): The id to use for this output component.
- **address** (*Optional*, int): Manually specify the I²C address of
  the DAC. Defaults to ``0x2E``.
- All other options from :ref:`Output <config-output>`.

See Also
--------

- :doc:`/components/output/mcp4725`
- :doc:`/components/output/esp32_dac`
- :doc:`/components/output/esp8266_pwm`
- :ghedit:`Edit`
