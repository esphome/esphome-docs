Jablotron Section Select
========================

.. seo::
    :description: Instructions for setting up a jablotron_section Select.

The `jablotron_section` select platform creates a Select for a section
configured in the Jablotron control panel. The select requires
:doc:`Jablotron Component </components/jablotron>` to be configured.

You must configure an access code, either on the parent Jablotron component,
or on the Select itself.

You can select the following values from the JA-121T protocol:

- ``READY``: Normal mode (unarmed)
- ``ARMED_PART``: Partially set
- ``ARMED``: Set

Configuration variables:
------------------------
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- **name** (*Required*, string): The name of the sensor.
- **index** (*Required*, int): Index of the section in the Jablotron control panel.
- **access_code** (*Optional*, string): Specify the access code. If empty, will use the 
  access code configured on the parent :doc:`Jablotron Component </components/jablotron>`.

Example

.. code-block:: yaml

    uart:
      # ...
    jablotron:
      # ...
    select:
      - platform: jablotron_section
        index: 1
        name: Main
        access_code: 5*4321


See Also
--------
- :apiclass:`:jablotron_section::SectionSelect`
- :doc:`/components/jablotron`
- :doc:`/components/text_sensor/jablotron_section`
- :doc:`/components/binary_sensor/jablotron_section_flag`
- :doc:`/components/uart`
- `JA-121 RS-485 Interface <https://jablotron.com.hk/image/data/pdf/manuel/JA-121T.pdf>`__
- :ghedit:`Edit`
