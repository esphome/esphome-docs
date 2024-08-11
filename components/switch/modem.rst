Modem Switch
============

.. seo::
    :description: Enable or disable modem characteristics.

The ``modem`` platform is a switch platform that can
enable or disable :doc:`/components/modem` for service characteristics.

.. note::

    The :doc:`/components/modem` must have ``enable_cmux`` set to **True**.


.. code-block:: yaml

    modem:
      id: atmodem
      rx_pin: GPIO26
      tx_pin: GPIO27
      status_pin: GPIO34
      model: SIM7600
      apn: orange
      enable_cmux: True

    switch:
      - platform: modem
        gnss:
          name: GNSS
          restore_mode: ALWAYS_ON

Configuration variables:
------------------------

- **gnss** (*Optional*): Enable/disable gnss. Only available for modem model ``SIM7600`` and ``SIM7670``. All options from
  :ref:`Switch <config-switch>`.

See Also
--------

- :doc:`/components/modem`
- :doc:`/components/sensor/modem`
- :ref:`sensor-filters`
- :ghedit:`Edit`
