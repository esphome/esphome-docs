Command Line Interface
======================

.. seo::
    :description: Documentation for the command line interface of esphomelib.

Base Usage
----------

esphomeyaml's command line interface always has the following format

.. code-block:: console

    esphomeyaml <CONFIGURATION> <COMMAND> [ARGUMENTS]


``run`` Command
---------------

The ``esphomeyaml <CONFIG> run`` command is the most common command for esphomeyaml. It

* Validates the configuration
* Compiles a firmware
* Uploads the firmware (over OTA or USB)
* Starts the log view

.. program:: esphomeyaml run

.. option:: --upload-port UPLOAD_PORT

    Manually specify the upload port/ip to use. For example ``/dev/cu.SLAB_USBtoUART``.

.. option:: --no-logs

    Disable starting log view.

.. option:: --topic TOPIC

    Manually set the topic to subscribe to for MQTT logs (defaults to the one in the configuration).

.. option:: --username USERNAME

    Manually set the username to subscribe with for MQTT logs (defaults to the one in the configuration).

.. option:: --password PASSWORD

    Manually set the password to subscribe with for MQTT logs (defaults to the one in the configuration).

.. option:: --client-id CLIENT_ID

    Manually set the client ID to subscribe with for MQTT logs (defaults to a randomly chosen one).

.. option:: --host-port HOST_PORT

    Specify the host port to use for legacy Over the Air uploads.

``config`` Command
------------------

.. program:: esphomeyaml config

The ``esphomeyaml <CONFIG> config`` validates the configuration and displays the validation result.

.. option:: --topic TOPIC

    Manually set the topic to subscribe to for MQTT logs (defaults to the one in the configuration).

.. option:: --username USERNAME

    Manually set the username to subscribe with for MQTT logs (defaults to the one in the configuration).

.. option:: --password PASSWORD

    Manually set the password to subscribe with for MQTT logs (defaults to the one in the configuration).

.. option:: --client-id CLIENT_ID

    Manually set the client ID to subscribe with for MQTT logs (defaults to a randomly chosen one).

.. option:: --serial-port SERIAL_PORT

    Manually specify the serial port to read the logs from. For example ``/dev/cu.SLAB_USBtoUART``.

``compile`` Command
-------------------

.. program:: esphomeyaml compile

The ``esphomeyaml <CONFIG> compile`` validates the configuration and compiles the firmware.

.. option:: --only-generate

    If set, only generates the C++ source code and does not compile the firmware.

``upload`` Command
------------------

.. program:: esphomeyaml upload

The ``esphomeyaml <CONFIG> upload`` validates the configuration and uploads the most recent firmware build.

.. option:: --upload-port UPLOAD_PORT

    Manually specify the upload port/ip to use. For example ``/dev/cu.SLAB_USBtoUART``.

.. option:: --host-port HOST_PORT

    Specify the host port to use for legacy Over the Air uploads.

``clean-mqtt`` Command
----------------------

.. program:: esphomeyaml clean-mqtt

The ``esphomeyaml <CONFIG> clean-mqtt`` cleans retained MQTT discovery messages from the MQTT broker.
See :ref:`mqtt-using_with_home_assistant`.

.. option:: --topic TOPIC

    Manually set the topic to clean retained messages from (defaults to the MQTT discovery topic of the
    node).

.. option:: --username USERNAME

    Manually set the username to subscribe with.

.. option:: --password PASSWORD

    Manually set the password to subscribe with.

.. option:: --client-id CLIENT_ID

    Manually set the client ID to subscribe with.

``wizard`` Command
------------------

.. program:: esphomeyaml wizard

The ``esphomeyaml <CONFIG> wizard`` command starts the esphomeyaml configuration creation wizard.

``mqtt-fingerprint`` Command
----------------------------

.. program:: esphomeyaml mqtt-fingerprint

The ``esphomeyaml <CONFIG> mqtt-fingerprint`` command shows the MQTT SSL fingerprints of the remote used
for SSL MQTT connections. See :ref:`mqtt-ssl_fingerprints`.

``version`` Command
-------------------

.. program:: esphomeyaml version

The ``esphomeyaml <CONFIG> version`` command shows the current esphomeyaml version and exits.

``clean`` Command
-----------------

.. program:: esphomeyaml clean

The ``esphomeyaml <CONFIG> clean`` command cleans all build files and can help with some build issues.

``hass-config`` Command
-----------------------

.. program:: esphomeyaml hass-config

The ``esphomeyaml <CONFIG> hass-config`` command shows an auto-generated Home Assistant configuration for the esphomeyaml
node configuration file. This is useful if you're not using MQTT discovery.

``dashboard`` Command
---------------------

.. program:: esphomeyaml dashboard

The ``esphomeyaml <CONFIG> dashboard`` command starts the esphomeyaml dashboard server for using esphomeyaml
through a graphical user interface.

.. option:: --port PORT

    Manually set the HTTP port to open connections on (defaults to 6052)

.. option:: --password PASSWORD

    The optional password to require for all requests.

.. option:: --open-ui

    If set, opens the dashboard UI in a browser once the server is up and running.



