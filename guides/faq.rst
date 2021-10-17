Frequently Asked Questions
==========================

.. seo::
    :description: Frequently asked questions in ESPHome.
    :image: question_answer.png

Tips for using ESPHome
----------------------

1. ESPHome supports (most of) `Home Assistant's YAML configuration directives
   <https://www.home-assistant.io/docs/configuration/splitting_configuration/>`__ like
   ``!include`` and ``!secret``. So you can store all your secret WiFi passwords and so on
   in a file called ``secrets.yaml`` within the directory where the configuration file is.

   For even more configuration templating, take a look at :ref:`config-substitutions`.

2. If you want to see how ESPHome interprets your configuration, run

   .. code-block:: bash

       esphome livingroom.yaml config

3. To view the logs from your node without uploading, run

   .. code-block:: bash

       esphome livingroom.yaml logs

4. You can always find the source ESPHome generates under ``<NODE_NAME>/src/``.

5. You can view the full list of command line interface options here: :doc:`/guides/cli`

6. Use :ref:`substitutions <config-substitutions>` to reduce repetition in your configuration files.

.. |secret| replace:: ``!secret``
.. _secret: https://www.home-assistant.io/docs/configuration/secrets/
.. |include| replace:: ``!include``
.. _include: https://www.home-assistant.io/docs/configuration/splitting_configuration/

.. _esphome-flasher:

I can't get flashing over USB to work.
--------------------------------------

ESPHome depends on the operating system the tool is running on to recognize
the ESP. This can sometimes fail. Common causes are that you did not install
the drivers (see note below) or you are trying to upload from a Docker container
and did not mount the ESP device into your container using ``--device=/dev/ttyUSB0``.

Starting with ESPHome 1.9.0, the ESPHome suite provides
`esphome-flasher <https://github.com/esphome/esphome-flasher>`__, a tool to flash ESPs over USB.

First, you need to get the firmware file to flash. For Hass.io add-on based installs you can
use the ``COMPILE`` button (click the overflow icon with the three dots) and then press
``Download Binary``. For command line based installs you can access the file under
``<CONFIG_DIR>/<NODE_NAME>/.pioenvs/<NODE_NAME>/firmware.bin``.

Then, install esphome-flasher by going to the `releases page <https://github.com/esphome/esphome-flasher/releases>`__
and downloading one of the pre-compiled binaries. Open up the application and select the serial port
you want to flash to (on windows you can use the "device manager" to check if it's the right one).

.. figure:: images/esphomeflasher-ui.png
    :align: center
    :width: 80%

Select the firmware binary and finally press "Flash ESP".

.. note::

    If the serial port is not showing up, you might not have the required drivers installed.
    ESPs usually ship with one of these two UART chips:

     * CP2102 (square chip): `driver <https://www.silabs.com/products/development-tools/software/usb-to-uart-bridge-vcp-drivers>`__
     * CH341: `driver <https://github.com/nodemcu/nodemcu-devkit/tree/master/Drivers>`__

.. note::

    If you're just seeing ``Connecting....____....`` on the screen and the flashing fails, that might
    be a sign that the ESP is defect or cannot be programmed. Please double check the UART wires
    are connected correctly if flashing using a USB to UART bridge. For some devices you need to
    keep pressing the BOOT button until flashing has begun (ie. Geekcreit DOIT ESP32 DEVKIT V1).

Help! Something's not working!!
-------------------------------

That's no good. Here are some steps that resolve some problems:

-  **If you're having WiFi problems**: See :ref:`wifi-problems`.
-  Enable verbose logs in the logger: section.
-  **Still an error?** Please file a bug report over in the `ESPHome issue tracker <https://github.com/esphome/issues>`__.
   I will take a look at it as soon as I can. Thanks!

.. _faq-bug_report:

How to submit an issue report
-----------------------------

First of all, thank you very much to everybody submitting issue reports! While I try to test ESPHome/yaml as much as
I can using my own hardware, I don't own every single device type and mostly only do tests with my own home automation
system. When doing some changes in the core, it can quickly happen that something somewhere breaks. Issue reports are a
great way for me to track and (hopefully) fix issues, so thank you!

For me to fix the issue quickly, there are some things that would be really helpful:

1.  **Just writing "X doesn't work" or "X gives bug" is not helpful!!!** Seriously, how do you expect
    help given just that information?
2.  A snippet of the code/configuration file used is always great to reproduce this issue.
    Please read `How to create a Minimal, Complete, and Verifiable example <https://stackoverflow.com/help/mcve>`__.
3.  If it's an I²C or hardware communication issue please also try setting the
    :ref:`log level <logger-log_levels>` to ``VERY_VERBOSE`` as it provides helpful information
    about what is going on.
4.  Please also include what you've already tried and didn't work as that can help us track down the issue.

You can find the issue tracker here https://github.com/esphome/issues

How do I update to the latest version?
--------------------------------------

It's simple. Run:

.. code-block:: bash

    pip install -U esphome
    # From docker:
    docker pull esphome/esphome:latest

And in Hass.io, there's a simple UPDATE button when there's an update available as with all add-ons

.. _faq-beta:

How do I update to the latest beta release?
-------------------------------------------

ESPHome has a beta release cycle so that new releases can easily be tested before
the changes are deployed to the stable channel. You can help test ESPHome (and use new features)
by installing the tested beta:

.. code-block:: bash

    # For pip-based installs
    pip install --pre -U esphome

    # For docker-based installs
    docker run [...] -it esphome/esphome:beta livingroom.yaml run

For Home Assistant supervised installs add the community addons beta repository by
adding
`https://github.com/hassio-addons/repository-beta <https://github.com/hassio-addons/repository-beta>`__
in Add-on store -> Repositories.

The beta docs are available at `beta.esphome.io <https://beta.esphome.io>`__

How do I use the latest bleeding edge version?
----------------------------------------------

First, a fair warning that the latest bleeding edge version is not always stable and might have issues.
If you find some, please do however report them if you have time :)

To install the dev version of ESPHome:

- In Hass.io: Add the ESPHome repository `https://github.com/esphome/hassio <https://github.com/esphome/hassio>`
  in Add-on store -> Repositories. Then install the add-on  ``ESPHome Dev``
- From ``pip``: Run ``pip install https://github.com/esphome/esphome/archive/dev.zip``
- From docker, use the `esphome/esphome:dev <https://hub.docker.com/r/esphome/esphome/tags?page=1&name=dev>`__ image

  .. code-block:: bash

      docker run [...] -it esphome:dev livingroom.yaml compile

The latest dev docs are here: `next.esphome.io <https://next.esphome.io/>`__

How do I use my Home Assistant secrets.yaml?
--------------------------------------------

If you want to keep all your secrets in one place, make a ``secrets.yaml`` file in the
esphome directory with these contents (so it pulls in the contents of your main Home Assistant
``secrets.yaml`` file from one directory higher):

.. code-block:: yaml

    <<: !include ../secrets.yaml


Does ESPHome support [this device/feature]?
-------------------------------------------

If it's not in :doc:`the docs </index>`, it's probably not
supported. However, I'm always trying to add support for new features, so feel free to create a feature
request in the `ESPHome feature request tracker <https://github.com/esphome/feature-requests>`__. Thanks!

I have a question... How can I contact you?
-------------------------------------------

Sure! I'd be happy to help :) You can contact me here:

-  `Discord <https://discord.gg/KhAMKrd>`__
-  `Home Assistant Community Forums <https://community.home-assistant.io/c/third-party/esphome>`__
-  ESPHome `issue <https://github.com/esphome/issues>`__ and
   `feature request <https://github.com/esphome/feature-requests>`__ issue trackers. Preferably only for issues and
   feature requests.
-  Alternatively, also under contact (at) esphome.io (NO SUPPORT!)

.. _wifi-problems:

My node keeps reconnecting randomly
-----------------------------------

Jep, that's a known issue. However, it seems to be very low-level and I don't really know
how to solve it. I'm working on possible workarounds for the issue but currently I do
not have a real solution.

Some steps that can help with the issue:

- If you're using a hidden WiFi network, make sure to enable ``fast_connect`` mode in the WiFi
  configuration (also sometimes helps with non-hidden networks)
- Give your ESP a :ref:`static IP <wifi-manual_ip>`.
- Set the ``power_save_mode`` to ``light`` in the ``wifi:`` config (only helps in some cases,
  in other it can make things worse). See :ref:`wifi-power_save_mode`.
- The issue seems to happen with cheap boards more frequently. Especially the "cheap" NodeMCU
  boards from eBay which sometimes have quite bad antennas.
- ESPHome reboots on purpose when something is not going right, e.g.
  :doc:`wifi connection cannot be made </components/wifi>` or
  :doc:`api connection is lost </components/api>` or
  :doc:`mqtt connection is lost </components/mqtt>`. So if you are facing this problem you'll need
  to explicitly set the ``reboot_timeout`` option to ``0s`` on the components being used.


Docker Reference
----------------

Install versions:

.. code-block:: bash

    # Stable Release
    docker pull esphome/esphome
    # Beta
    docker pull esphome/esphome:beta
    # Dev version
    docker pull esphome/esphome:dev

Command reference:

.. code-block:: bash

    # Start a new file wizard for file livingroom.yaml
    docker run --rm -v "${PWD}":/config -it esphome/esphome livingroom.yaml wizard

    # Compile and upload livingroom.yaml
    docker run --rm -v "${PWD}":/config -it esphome/esphome livingroom.yaml run

    # View logs
    docker run --rm -v "${PWD}":/config -it esphome/esphome livingroom.yaml logs

    # Map /dev/ttyUSB0 into container
    docker run --rm -v "${PWD}":/config --device=/dev/ttyUSB0 -it esphome/esphome ...

    # Start dashboard on port 6052 (general command)
    # Warning: this command is currently not working with Docker on MacOS. (see note below)
    docker run --rm -v "${PWD}":/config --net=host -it esphome/esphome

    # Start dashboard on port 6052 (MacOS specific command)
    docker run --rm -p 6052:6052 -e ESPHOME_DASHBOARD_USE_PING=true -v "${PWD}":/config -it esphome/esphome

    # Setup a bash alias:
    alias esphome='docker run --rm -v "${PWD}":/config --net=host -it esphome/esphome'

And a docker compose file looks like this:

.. code-block:: yaml

    version: '3'

    services:
      esphome:
        image: esphome/esphome
        volumes:
          - ./:/config:rw
          # Use local time for logging timestamps
          - /etc/localtime:/etc/localtime:ro
        network_mode: host
        restart: always

.. note::

    ESPHome uses mDNS to show online/offline state in the dashboard view. So for that feature
    to work you need to enable host networking mode

    On MacOS the networking mode ("-net=host" option) doesn't work as expected. You have to use
    another way to launch the dashboard with a port mapping option and use alternative to mDNS
    to have the online/offline stat (see below)

    mDNS might not work if your Home Assistant server and your ESPHome nodes are on different subnets.
    If your router supports Avahi, you are able to get mDNS working over different subnets.

    Just follow the next steps:

    1. Enable Avahi on both subnets.
    2. Enable UDP traffic from ESPHome node's subnet to 224.0.0.251/32 on port 5353.

    Alternatively, you can make esphome use ICMP pings to check the status of the device
    with the Hass.io Addon ``"status_use_ping": true,`` option or with docker ``-e ESPHOME_DASHBOARD_USE_PING=true``
    See also https://github.com/esphome/issues/issues/641#issuecomment-534156628.

Can Configuration Files Be Recovered From The Device?
-----------------------------------------------------

If you lost your ESPHome YAML configuration files, there's no way to recover them.
The configuration is *not* stored on the device directly - only the generated firmware is on
the device itself (technically, the configuration can be reverse-engineered from that, but only
with a lot of work).

Always back up all your files!

See Also
--------

- :doc:`ESPHome index </index>`
- :doc:`contributing`
- :ghedit:`Edit`
