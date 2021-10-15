Sharing ESPHome devices
=======================

.. seo::
    :description: Information for creating and sharing devices using ESPHome firmware.

We have added configuration options to ESPHome to make it easier for everyone
to create, configure, install and distribute devices running ESPHome.

Example configuration
---------------------

.. code-block:: yaml

    esphome:
      ...
      # Automatically add the mac address to the name
      # so you can use a single firmware for all devices
      name_add_mac_suffix: true

      # This will allow for (future) project identification,
      # configuration and updates.
      project:
        name: jesse.temperature_monitor
        version: "1.0"

    # This should point to the public location of this yaml file.
    dashboard_import:
      package_import_url: github://jesserockz/dummy-esphome-configs@v1/temperature-monitor.yaml

    wifi:
      # Set up a wifi access point
      ap:
        ssid: jesses_temperature_monitor
        password: 12345678

    # In combination with the `ap` this allows the user
    # to provision wifi credentials to the device.
    captive_portal:

    # Sets up Bluetooth LE (Only on ESP32) to allow the user
    # to provision wifi credentials to the device.
    esp32_improv:
      authorizer: none


Relevant Documentation
----------------------

- ``name_add_mac_suffix`` - :ref:`esphome-mac_suffix`
- ``project`` - :ref:`esphome-creators_project`
- ``esp32_improv`` - :doc:`/components/esp32_improv`
- ``captive_portal`` - :doc:`/components/captive_portal`
- ``wifi`` -> ``networks: []`` allows you to flash a device that will not contain any
  credentials and they must be set by the user via either the ``ap`` + ``captive_portal`` or
  the ``esp32_improv`` components.
- ``dashboard_import`` -> ``package_import_url`` - This should point to the public repository containing
  the configuration for the device so that the user's ESPHome dashboard can auto detect this device and
  create a minimal yaml using :ref:`config-git_packages`.

See Also
--------

- :ghedit:`Edit`
