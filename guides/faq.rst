Frequently Asked Questions
==========================

.. seo::
    :description: Frequently asked questions in ESPHome.
    :image: question_answer.svg

Tips for using ESPHome
----------------------

1. ESPHome supports (most of) `Home Assistant's YAML configuration directives
   <https://www.home-assistant.io/docs/configuration/splitting_configuration/>`__ like
   ``!include`` and ``!secret``. So you can store all your secret WiFi passwords and so on
   in a file called ``secrets.yaml`` within the directory where the configuration file is.

   For even more configuration templating, take a look at :ref:`config-substitutions`.

2. If you want to see how ESPHome interprets your configuration, run

   .. code-block:: bash

       esphome config livingroom.yaml

3. To view the logs from your node without uploading, run

   .. code-block:: bash

       esphome logs livingroom.yaml

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

First, you need to get the firmware file to flash. For the Home Assistant add-on based
installs you can use the ``COMPILE`` button (click the overflow icon with the three dots)
and then press ``Download Binary``. For command line based installs you can access the
file under ``<CONFIG_DIR>/<NODE_NAME>/.pioenvs/<NODE_NAME>/firmware.bin``.

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
   We will take a look at it as soon as we can. Thanks!

.. _faq-bug_report:

How to submit an issue report
-----------------------------

First of all, thank you very much to everybody submitting issue reports! While we try to test ESPHome/YAML as much as
we can using our available hardware, we don't own every single device type and rely on testing done by the community 
and the contributors. When doing some changes in the core, it can quickly happen that something somewhere breaks. 
Issue reports are a great way for us to track and (hopefully) fix issues, so thank you!

For us to fix the issue quickly, there are some things that would be really helpful:

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

    pip3 install -U esphome
    # From docker:
    docker pull esphome/esphome:latest

And in Home Assistant, there's a simple UPDATE button when there's an update
available as with all add-ons.

.. _faq-beta:

How do I update to the latest beta release?
-------------------------------------------

ESPHome has a beta release cycle so that new releases can easily be tested before
the changes are deployed to the stable channel. You can help test ESPHome (and use new features)
by installing the tested beta:

.. code-block:: bash

    # For pip-based installs
    pip3 install --pre -U esphome

    # For docker-based installs
    docker run [...] -it esphome/esphome:beta run livingroom.yaml

For Home Assistant supervised installs add the community addons beta repository by
adding
`https://github.com/hassio-addons/repository-beta <https://github.com/hassio-addons/repository-beta>`__
in Add-on store -> Repositories.

The beta docs are available at `beta.esphome.io <https://beta.esphome.io>`__

How do I use the latest bleeding edge version?
----------------------------------------------

First, a fair warning that the latest bleeding edge version is not always stable and might have issues.
If you find some, please do however report them.

To install the dev version of ESPHome:

- In Home Assistant: Add the ESPHome repository `https://github.com/esphome/hassio <https://github.com/esphome/hassio>`__
  in Add-on store -> Repositories. Then install the add-on  ``ESPHome Dev``
- From ``pip``: Run ``pip3 install https://github.com/esphome/esphome/archive/dev.zip``
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
supported. However, we are always trying to add support for new features, so feel free to create a feature
request in the `ESPHome feature request tracker <https://github.com/esphome/feature-requests>`__. Thanks!

I have a question... How can I contact you?
-------------------------------------------

Sure! We are happy to help :) You can contact us here:

-  `Discord <https://discord.gg/KhAMKrd>`__
-  `Home Assistant Community Forums <https://community.home-assistant.io/c/third-party/esphome>`__
-  ESPHome `issue <https://github.com/esphome/issues>`__ and
   `feature request <https://github.com/esphome/feature-requests>`__ issue trackers. Preferably only for issues and
   feature requests.
-  Alternatively, also under contact (at) esphome.io (NO SUPPORT!)

.. _wifi-problems:

My node keeps reconnecting randomly
-----------------------------------

Jep, that's a known issue. However, it seems to be very low-level and we don't really know
how to solve it. We are working on possible workarounds for the issue, but currently we do
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
- If you see ``Error: Disconnecting <NODE_NAME>`` in your logs, ESPHome is actively closing
  the native API client connection. Connect a serial console to inspect the reason, which is only
  logged via serial. If you see ``ack timeout 4`` right before a disconnect, this might be because
  of a bug in the AsyncTCP library, for which a fix was included in ESPHome version 1.18.0.
  If you are running an ESPHome version, prior to 1.18.0, then upgrade ESPHome and build fresh
  firmware for your devices. 
- We have seen an increase in disconnects while the log level was set to ``VERY_VERBOSE``,
  especially on single-core devices, where the logging code might be interfering with the operation
  of the networking code. For this reason, we advise using a lower log level for production
  purposes.
- Related to this, seems to be the number of clients that are simultaneously connected to the native
  API server on the device. These might for example be Home Assistant (via the ESPHome integration) and
  the log viewer on the web dashboard. In production, you will likely only have a single connection from
  Home Assistant, making this less of an issue. But beware that attaching a log viewer might
  have impact.

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
    docker run --rm -v "${PWD}":/config -it esphome/esphome wizard livingroom.yaml

    # Compile and upload livingroom.yaml
    docker run --rm -v "${PWD}":/config -it esphome/esphome run livingroom.yaml

    # View logs
    docker run --rm -v "${PWD}":/config -it esphome/esphome logs livingroom.yaml

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

.. _docker-reference-notes:
.. note::

    By default ESPHome uses mDNS to show online/offline state in the dashboard view. So for that feature
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
    with the Home Assistant add-on ``"status_use_ping": true,`` option or with
    Docker ``-e ESPHOME_DASHBOARD_USE_PING=true``.
    See also https://github.com/esphome/issues/issues/641#issuecomment-534156628.
    
.. _faq-notes_on_disabling_mdns:

Notes on disabling mDNS
------------------------------------------------------------------------------
Some of ESPHome's functionalities rely on mDNS, so naturally :ref:`disabling <wifi-configuration_variables>` it will cause these features to stop working.
Generally speaking, disabling mDNS without setting a :ref:`static IP address <wifi-manual_ip>` (or a static DHCP lease) is bound to cause problems. This is due to the fact that mDNS is used to find the IP address of each ESPHome nodes.

- You will not be able to use the node's hostname to ping, find it's IP address or connect to it.

- Automatic discovery in Home Assistant when using :doc:`native API </components/api>` relies on mDNS broadcast messages to detect presence of new ESPHome nodes. If you need to use the native API with mDNS disabled, then you will have to use a static IP address and manually add the ESPHome integration with the fixed IP address.

- Online status detection in ESPHome's dashboard by default uses mDNS, so disabling mDNS will cause the ESPHome dashboard to show the status of the nodes created without mDNS support to be always offline. Currently, this does not affect any functionality, however if you want to see the online/offline status you could configure ESPHome to ping each node instead. See the :ref:`notes in the Docker Reference section <docker-reference-notes>` for more information.

Can Configuration Files Be Recovered From The Device?
-----------------------------------------------------

If you lost your ESPHome YAML configuration files, there's no way to recover them.
The configuration is *not* stored on the device directly - only the generated firmware is on
the device itself (technically, the configuration can be reverse-engineered from that, but only
with a lot of work).

Always back up all your files!


Why shouldn't I use underscores in my device name?
--------------------------------------------------

The top level ``name:`` field in your .yaml file defines the node name(/hostname) on the local network.  According to `RFC1912 <https://datatracker.ietf.org/doc/html/rfc1912>`_, underscore characters (``_``) in hostnames are not valid.  In reality some local DNS/DHCP setups will be ok with underscores and some will not.  If connecting via a static IP address, there will probably be no issues.  In some cases, initial setup using an underscore works, but later the connection might fail when Home Assistant restarts or if you change router hardware.  Recommendation: use hyphen (``-``) instead of underscore if you can.  

Important: follow these `instructions </components/esphome.html#changing-esphome-node-name>`_ to use the ``use_address`` parameter when renaming a live device, as the connection to an existing device will only work with the old name until the name change is complete.

Why am I getting a warning about strapping pins?
--------------------------------------------------

The ESP chips have special "strapping pins" that are read during the bootup procedure and determine how it boots up. They define whether the ESP boots into a special "flashing mode" or normal boot and a couple of other internal settings.
If an external pullup/down changes the configured voltage levels boot failures or hard to diagnose issues can happen.
While the use of them in software is not a problem, if there's something attached to the pins (particularly if they're not floating during the bootup) you may run into problems.
It's recommended to avoid them unless you have a pressing need to use them and you have reviewed the expected boot voltage levels of these pins from the ESP datasheet.

Note that some boards connect pins such as GPIO0 to a builtin tactile switch. In these cases using the strapping pins is not a problem.

How can I test a Pull Request?
------------------------------

By leveraging the :doc:`external components </components/external_components>` feature, it's possible to test most Pull 
Requests by simply adding a few lines to your YAML! You need the number of the Pull Request, as well as the components 
that have been added or changed by the Pull Request (they are listed with the "integration:" labels on the GitHub page 
of the Pull Request). Then, if you add a block of code like the following to your YAML file, once you recompile and 
flash your device, the code from the Pull Request will be used for the components changed by the Pull Request.

.. code-block:: yaml

    external_components:
      # replace 1234 with the number of the Pull Request
      - source: github://pr#1234
        components:
          # list all components modified by this Pull Request here
          - ccs811  


Note that this only works for Pull Requests that only change files within components. If any files outside 
``esphome/components/`` are added or changed, this method unfortunately doesn't work. Those Pull Requests are labeled 
with the "core" label on GitHub.

See Also
--------

- :doc:`ESPHome index </index>`
- :doc:`contributing`
- :ghedit:`Edit`
