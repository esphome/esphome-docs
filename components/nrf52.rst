NRF52 Platform
===============

.. seo::
    :description: Configuration for the NRF52 platform for ESPHome.
    :image: nrf52.svg

This component contains platform-specific options for the NRF52 platform.

.. note::

    Support for all aspects of ESPHome on the NRF52 is still in development.

.. code-block:: yaml

    # Example configuration entry
    nrf52:
        board: adafruit_feather_nrf52840

Configuration variables:
------------------------

- **board** (*Required*, string): The board type. Valid options are ``adafruit_feather_nrf52840`` and ``adafruit_itsybitsy_nrf52840``. Other boards should work with those configuration as well.

Getting Started
---------------

The nRF52840 requires a bootloader, with two supported options: ``MCUboot`` and ``Adafruit nRF52 Bootloader``. It is recommended to use MCUboot as it supports OTA (Over-The-Air) updates. Your board most likely comes with a manufacturer-provided bootloader. ESPHome determines the bootloader type based on the board name.

Examples of low power `nRF52840 boards <https://github.com/joric/nrfmicro/wiki>`__.


Flashing with MCUboot
----------------------

Flashing this bootloader requires an SWD connection, for which a programmer is necessary. A cheap ST-Link V2 can be utilized.

1. Connect the board to the PC via SWD.
2. Run ``esphome upload yourfile.yaml --device PYOCD``.

.. code-block:: yaml

    # Example configuration entry
    nrf52:
        board: adafruit_feather_nrf52840

Flashing with Adafruit nRF52 Bootloader
---------------------------------------

This bootloader supports updates over USB CDC.

1. Connect the board to the PC via USB.
2. Quickly short the reset pin to ground twice.
3. Run ``esphome upload yourfile.yaml``.

.. code-block:: yaml

    # Example configuration entry
    nrf52:
        board: adafruit_itsybitsy_nrf52840

GPIO Pin Numbering
------------------

There are two ways to reference GPIO pins:

1. By pin name, e.g., ``P0.15`` or ``P1.11``.
2. By pin number, e.g., ``15`` or ``43``.

See Also
--------

- :doc:`esphome`
- :ghedit:`Edit`
