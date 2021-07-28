Anova Cooker
=============

.. seo::
    :description: Instructions for setting up an Anova sous-vide cooker.
    :image: anova.png

The ``anova`` climate platform creates a climate device which can be used
to control a BLE Anova sous-vide stick. Whilst not strictly a climate
device, the concept of keeping something to a set temperature applies
equally here.

This component supports the following functionality:

- Turn the stick on or off
- Set the desired temperature
- Show the current temperature

The timer is not currently supported, you can use automations to achieve
similar functionality.

This platform uses the BLE peripheral on an ESP32, so you also need to enable
this component. Please see the BLE Client docs for how to discover the MAC
address of your Anova device.
You cannot use the Anova app over BLE whilst this component is connected, you
should disconnect it first. To setup a (dis-)connect switch, see :doc:`/components/switch/ble_client`.

.. code-block:: yaml

    ble_client:
      - mac_address: 11:22:33:aa:bb:cc
        id: my_anova

    climate:
      - platform: anova
        name: "My Anova stick"
        ble_client_id: my_anova

Configuration variables:
------------------------

- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- **name** (**Required**, string): The name of the climate device.
- **ble_client_id** (**Required**, :ref:`config-id`): The ID of the BLE Client.
- All other options from :ref:`Climate <config-climate>`.

See Also
--------

- :doc:`/components/ble_client`
- :doc:`/components/climate/index`
- :apiref:`anova/anova.h`
- :ghedit:`Edit`
