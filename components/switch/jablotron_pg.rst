Jablotron PG Switch
===================

.. seo::
    :description: Instructions for setting up a jablotron_pg switch.

The `jablotron_pg` switch platform creates a Sensor for a PG output
configured in the Jablotron control panel. The switch requires
:doc:`Jablotron Component </components/jablotron>` to be configured.

You must configure an access code, either on the parent Jablotron component,
or on the Switch itself. The user has to have permission to set the PG output.

Configuration variables:
------------------------
- **name** (*Required*, string): The name of the switch.
- **index** (*Required*, int): Index of the PG output in the Jablotron control panel.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- **jablotron_id** (*Optional*, :ref:`config-id`): Manually specify the ID of the :doc:`Jablotron Component </components/jablotron>` to be used.
- **access_code** (*Optional*, string): Specify the access code. If empty, will use the 
  access code configured on the parent :doc:`Jablotron Component </components/jablotron>`.

All other options from :ref:`Switch component <config-switch>`.

Example

.. code-block:: yaml

    uart:
      # ...
    jablotron:
      # ...
    switch:
      - platform: jablotron_pg
        index: 12
        name: Sprinkler



See Also
--------
- :apiclass:`:jablotron_pg::PGSwitch`
- :doc:`/components/jablotron`
- :doc:`/components/uart`
- `JA-121 RS-485 Interface <https://jablotron.com.hk/image/data/pdf/manuel/JA-121T.pdf>`__
- :ghedit:`Edit`
