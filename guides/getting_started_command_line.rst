Getting Started with the ESPHome Command Line
=============================================

.. seo::
    :description: Getting Started guide for installing ESPHome using the command line and creating a basic configuration.
    :image: console.svg

ESPHome is the perfect solution for creating custom firmwares for
your ESP8266/ESP32 boards. In this guide we’ll go through how to set up a
basic “node” in a few simple steps.

Installation
------------

See :doc:`installing_esphome`.

If you're familiar with Docker, you can use that instead! Our image supports
AMD64, ARM and ARM64 (AARCH64), and can be downloaded with:

.. code-block:: bash

    docker pull esphome/esphome

Connecting the ESP Device
-------------------------

Follow the instructions in :doc:`physical_device_connection` to connect to your
ESP device.

.. note::

    The most difficult part of setting up a new ESPHome device is the initial
    installation. Installation requires that your ESP device is connected with
    a cable to a computer. Later updates can be installed wirelessly.

Creating a Project
------------------

Now let’s setup a configuration file. Fortunately, ESPHome has a
friendly setup wizard that will guide you through creating your first
configuration file. For example, if you want to create a configuration
file called ``livingroom.yaml``:

.. code-block:: bash

    esphome wizard livingroom.yaml
    # On Docker:
    docker run --rm -v "${PWD}":/config -it esphome/esphome wizard livingroom.yaml

At the end of this step, you will have your first YAML configuration
file ready. It doesn't do much yet and only makes your device connect to
the WiFi network, but still it’s a first step.

Adding some features
--------------------

So now you should have a file called ``livingroom.yaml`` (or similar).
Go open that file in an editor of your choice and let’s add a :doc:`simple
GPIO switch </components/switch/gpio>` to our app.

.. code-block:: yaml

    switch:
      - platform: gpio
        name: "Living Room Dehumidifier"
        pin: 5

The configuration format should hopefully immediately seem similar to
you. ESPHome has tried to keep it as close to Home Assistant’s
``configuration.yaml`` schema as possible. In the above example, we’re
simply adding a switch that’s called “Living Room Dehumidifier” (could control
anything really, for example lights) and is connected to pin ``GPIO5``.
The nice thing about ESPHome is that it will automatically also try
to translate pin numbers for you based on the board. For example in the
above configuration, if using a NodeMCU board, you could have just as
well set ``D1`` as the ``pin:`` option.

First uploading
---------------

Now you can go ahead and add some more components. Once you feel like
you have something you want to upload to your ESP board, simply plug in
the device via USB and type the following command (replacing
``livingroom.yaml`` with your configuration file):

.. code-block:: bash

    esphome run livingroom.yaml

You should see ESPHome validating the configuration and telling you
about potential problems. Then ESPHome will proceed to compile and
upload the custom firmware. You will also see that ESPHome created a
new folder with the name of your node. This is a new PlatformIO project
that you can modify afterwards and play around with.

If you are running docker on Linux you can add ``--device=/dev/ttyUSB0``
to your docker command to map a local USB device.

.. code-block:: bash

    docker run --rm -v "${PWD}":/config --device=/dev/ttyUSB0 -it esphome/esphome run livingroom.yaml

Now when you go to the Home Assistant "Integrations" screen (under "Configuration" panel), you
should see the ESPHome device show up in the discovered section (although this can take up to 5 minutes).
Alternatively, you can manually add the device by clicking "CONFIGURE" on the ESPHome integration
and entering "<NODE_NAME>.local" as the host.

.. figure:: /components/switch/images/gpio-ui.png
    :align: center

After the first upload, you will probably never need to use the USB
cable again, as all features of ESPHome are enabled remotely as well.
No more opening hidden boxes stowed in places hard to reach. Yay!

Adding A Binary Sensor
----------------------

Next, we’re going to add a very simple binary sensor that periodically
checks if a particular GPIO pin is pulled high or low - the :doc:`GPIO Binary
Sensor </components/binary_sensor/gpio>`.

.. code-block:: yaml

    binary_sensor:
      - platform: gpio
        name: "Living Room Window"
        pin:
          number: 16
          inverted: true
          mode:
            input: true
            pullup: true

This is an advanced feature of ESPHome. Almost all pins can
optionally have a more complicated configuration schema with options for
inversion and pinMode - the :ref:`Pin Schema <config-pin_schema>`.

This time when uploading, you don’t need to have the device plugged in
through USB again. The upload will magically happen “over the air”.
Using ESPHome directly, this is the same as from a USB cable, but
for docker you need to supply an additional parameter:

.. code-block:: bash

    esphome livingroom.yaml run
    # On docker
    docker run --rm -v "${PWD}":/config -it esphome/esphome run livingroom.yaml

.. figure:: /components/binary_sensor/images/gpio-ui.png

Where To Go Next
----------------

Great 🎉! You’ve now successfully set up your first ESPHome project
and uploaded your first ESPHome custom firmware to your node. You’ve
also learned how to enable some basic components via the configuration
file.

So now is a great time to go take a look at the :doc:`Components Index </index>`.
Hopefully you’ll find all sensors/outputs/etc. you’ll need in there. If you’re having any problems or
want new features, please either create a new issue on the `GitHub issue
tracker <https://github.com/esphome/issues/issues>`__ or find us on the
`Discord chat <https://discord.gg/KhAMKrd>`__ (also make sure to read the :doc:`FAQ <faq>`).

Bonus: ESPHome dashboard
------------------------

ESPHome features a dashboard that you can use to easily manage your nodes
from a nice web interface. It was primarily designed for
:doc:`the Home Assistant add-on <getting_started_hassio>`, but also works with a simple command on
\*nix machines (sorry, no windows).

To start the ESPHome dashboard, simply start ESPHome with the following command
(with ``config/`` pointing to a directory where you want to store your configurations)

.. code-block:: bash

    # Install dashboard dependencies
    pip install tornado esptool
    esphome dashboard config/

    # On Docker, host networking mode is required for online status indicators
    docker run --rm --net=host -v "${PWD}":/config -it esphome/esphome

    # On Docker with MacOS, the host networking option doesn't work as expected. An
    # alternative is to use the following command if you are a MacOS user.
    docker run --rm -p 6052:6052 -e ESPHOME_DASHBOARD_USE_PING=true -v "${PWD}":/config -it esphome/esphome


After that, you will be able to access the dashboard through ``localhost:6052``.

.. figure:: images/dashboard_states.png

See Also
--------

- :doc:`cli`
- :doc:`ESPHome index </index>`
- :doc:`getting_started_hassio`
- :ghedit:`Edit`
