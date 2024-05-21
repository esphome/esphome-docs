.. _made_for_esphome:

Made for ESPHome
================

.. seo::
    :description: Information about the Made for ESPHome program
    :image: /_static/made-for-esphome-black-on-white.png

ESPHome has a wonderful and active community that loves creating and sharing projects.
You can apply for your project to get the ``Made for ESPHome`` stamp of approval.
This ensures that your project is powered by ESPHome and guarantees a minimum level of customizability to users.

Requirements
------------

There are a number of requirements your project must meet. These may vary based on its design. They are:

For projects which utilize Wi-Fi
********************************

Wi-Fi is quite common but requires configuration of the SSID and passphrase.
As such, for easy end-user provisioning, your configuration must include:

- ``esp32_improv`` as described in :doc:`/components/esp32_improv`
- ``improv_serial`` as described in :doc:`/components/improv_serial`, if a USB connection is available (recommended)

Note that these are **not** required for projects that only provide a physical/wired Ethernet port for connectivity.

For all projects
****************

- Your project is powered by ESPHome (runs ESPHome as its firmware)
- Your project is powered by an ESP32 or *supported* ESP32 variant such as the S2, S3, C3, etc.
- Your ESPHome configuration is open source, available for end users to modify/update
- Users should be able to apply updates if your project sells ready-made devices
- Your project supports adoption via the ``dashboard_import`` feature of ESPHome (see :doc:`Sharing </guides/creators>`). In particular:
    - There are **no** references to secrets or passwords
    - Network configuration must assume defaults (no static IPs or DNS configured)
    - It **must** compile successfully without any user changes after adopting it.
    - All configuration is contained within a single YAML file. Fully remote packages are permitted if using ``import_full_config: true``.

- Your product name cannot contain **ESPHome** except in the case of *ending with* **for ESPHome**

When your project matches all requirements of the Made for ESPHome program,
you can apply for permission to carry the logo by emailing esphome@nabucasa.com

Logos
-----

.. raw:: html

    <style>
        .transparent-background img {
            background: repeating-conic-gradient(#999 0% 25%, transparent 10% 50%) 50% / 10px 10px;
        }
    </style>

.. figure:: /_static/made-for-esphome-black-on-white.svg
    :align: center
    :width: 100%
    :class: transparent-background

    Made with ESPHome black on white (`svg </_static/made-for-esphome-black-on-white.svg>`__, `png </_static/made-for-esphome-black-on-white.png>`__)

.. figure:: /_static/made-for-esphome-white-on-black.svg
    :align: center
    :width: 100%
    :class: transparent-background

    Made with ESPHome white on black (`svg </_static/made-for-esphome-white-on-black.svg>`__, `png </_static/made-for-esphome-white-on-black.png>`__)

.. figure:: /_static/made-for-esphome-black-on-transparent.svg
    :align: center
    :width: 100%
    :class: transparent-background

    Made with ESPHome black on transparent (`svg </_static/made-for-esphome-black-on-transparent.svg>`__, `png </_static/made-for-esphome-black-on-transparent.png>`__)

.. figure:: /_static/made-for-esphome-white-on-transparent.svg
    :align: center
    :width: 100%
    :class: transparent-background

    Made with ESPHome white on transparent (`svg </_static/made-for-esphome-white-on-transparent.svg>`__, `png </_static/made-for-esphome-white-on-transparent.png>`__)
