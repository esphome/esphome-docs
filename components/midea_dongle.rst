Midea Dongle
============

.. seo::
    :description: Instructions for setting up the Midea Dongle component
    :image: midea.svg
    :keywords: midea

The ``midea_dongle`` component creates a serial connection to the Midea climate devices for others components to use.

.. note::

    This protocol also used by some vendors:

        - `Electrolux <https://www.electrolux.ru/>`_
        - `Qlima <https://www.qlima.com/>`_
        - `Artel <https://www.artelgroup.com/>`_
        - `Carrier <https://www.carrier.com/>`_
        - `Comfee <http://www.comfee-russia.ru/>`_
        - `Inventor <https://www.inventorairconditioner.com/>`_
        - and maybe others

    Example of hardware implementation is `Midea Open Dongle <https://github.com/dudanov/midea-open-dongle>`_ in free `KiCad <https://kicad-pcb.org>`_ format.

As the communication with Midea devices done using UART, you need
to have an :doc:`uart` in your configuration.
Additionally, you need to set the baud rate to 9600.

.. code-block:: yaml

    # Example configuration entry
    # Disable logging over UART
    logger:
      baud_rate: 0

    uart:
      tx_pin: 1
      rx_pin: 3
      baud_rate: 9600

    midea_dongle:

    midea_ac:
      name: "Midea AC"
      beeper: true

.. note::

    The configuration above should work for :doc:`climate/midea_ac`.

Configuration variables:
------------------------

- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- **uart_id** (*Optional*, :ref:`config-id`): Manually specify the ID of the :doc:`uart` if you want
  to use multiple UART buses.
- **stratched_icon** (*Optional*, bool, default: **false**): Set if your device have signal stretched icon
  and you want to use this feature. By default, on connected state, icon show maximum signal quality.

Acknowledgments:
----------------

Thanks to the following people for their contributions to reverse engineering the UART protocol and source code in the following repositories:

* `Mac Zhou <https://github.com/mac-zhou/midea-msmart>`_
* `NeoAcheron <https://github.com/NeoAcheron/midea-ac-py>`_
* `Rene Klootwijk <https://github.com/reneklootwijk/node-mideahvac>`_

See Also
--------

- :apiref:`midea_dongle/midea_dongle.h`
- :ghedit:`Edit`
