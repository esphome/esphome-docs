Contributing
============

Contributions to the esphomelib suite are very welcome! All the code for the projects
is hosted on GitHub and you can find the sources here:

- `esphomelib <https://github.com/OttoWinter/esphomelib>`__ (The C++ framework)
- `esphomeyaml <https://github.com/OttoWinter/esphomeyaml>`__ (The Python YAML to C++ transpiler)
- `esphomedocs <https://github.com/OttoWinter/esphomedocs>`__ (The documentation which you're reading here)

Just clone the repository locally, do the changes for your new feature/bugfix and submit
a pull request. I will try to take a look at your PR as soon as possible.

Contributing to esphomedocs
---------------------------

One of the areas of esphomelib that can always be improved is the documentation.
If you see an issue somewhere, or spelling mistakes or if you want to share your awesome
setup, please feel free to submit a pull request.

The esphomelib documentation is built using `sphinx <http://www.sphinx-doc.org/>`__ and uses
`reStructuredText <http://docutils.sourceforge.net/rst.html>`__ for all source files.

In my opinion, markdown would have been the much better choice in hindsight, but at the time
I was setting up the documentation good doxygen integration was key to me. Anyway, here's a quick
RST primer:

- **Headers**: You can write titles like this:

  .. code:: rst

      My Title
      ========

  and section headers like this:

  .. code:: rst

      My Sub Section
      --------------

  and sub-section headers like this:

  .. code:: rst

      My Sub-sub section
      ******************

- **Links**: To create a link to an external resource (for example https://www.google.com), use
  ``\`Link text <link_url>\`__``. For example:

  .. code:: rst

      `Google.com <https://www.google.com>`__

  `Google.com <https://www.google.com>`__

- **References**: To reference another document, use the ``:doc:`` and ``:ref:`` roles (references
  are set up globally and can be used between documents):

  .. code:: rst

      .. _my-reference-label:

      Section to cross-reference
      ^^^^^^^^^^^^^^^^^^^^^^^^^^

      See :ref:`my-reference-label`, also see :doc:`/esphomeyaml/components/switch/gpio`.
      :doc:`Using custom text </esphomeyaml/components/switch/gpio>`.

  See :ref:`devices`, also see :doc:`/esphomeyaml/components/switch/gpio`.
  :doc:`Using custom text </esphomeyaml/components/switch/gpio>`.

- **Inline code**: To have text appear ``like this``, use double backticks:

  .. code:: rst

      To have text appear ``like this``, use double backticks.

  To have text appear ``like this``, use double backticks.

- **Code blocks**: To show a sample configuration file, use the ``code`` directive:

  .. code:: rst

      .. code:: yaml

          # Sample configuration entry
          switch:
            - platform: gpio
              name: "Relay #42"
              pin: GPIO13

  .. code:: yaml

        # Sample configuration entry
        switch:
          - platform: gpio
            name: "Relay #42"
            pin: GPIO13

  .. note::

      The YAML syntax highlighter is currently broken. Somehow sphinx thinks this should be
      C++ code 🤯. If you know how to fix this, it would be very much appreciated 😉

- **Images**: To show images, use the ``figure`` directive:

  .. code:: rst

      .. figure:: images/dashboard.png
          :align: center
          :width: 40.0%

          Optional figure caption.

  .. figure:: images/dashboard.png
     :align: center
     :width: 40.0%

     Optional figure caption.

- **Notes and warnings**: You can create simple notes and warnings using the ``note`` and ``warning``
  directives:

  .. code:: rst

      .. note::

           This is a note.

      .. warning::

           This is a warning.

  .. note::

       This is a note.

  .. warning::

       This is a warning.

- **Italic and boldface font families**: To *italicize* text, use one asterisk around the text. To put
  **a strong emphasis** on a piece of text, put two asterisks around it.

  .. code:: rst

      *This is italicized.* (A weird word...)
      **This is very important.**

  *This is italicized.* (A weird word...)
  **This is very important.**

- **Ordered and unordered list**: The syntax for lists in RST is more or less the same as in markdown:

  .. code:: rst

      - Unordered Item

        - Unordered Sub-Item

      - Item with a very long text so that it does not fully fit in a single line and
        must be split up into multiple lines.

      1. Ordered Item #1
      2. Ordered Item #2

  - Unordered Item

    - Unordered Sub-Item

  - Item with a very long text so that it does not fully fit in a single line and
    must be split up into multiple lines.

  1. Ordered Item #1
  2. Ordered Item #2

reStructured text can do a lot more than this, so if you're looking for a more complete guide
please have a look at the `Sphinx reStructuredText Primer <http://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html>`__.

To check your documentation changes locally, you first need install sphinx (**with Python 3**) and
`doxygen <http://www.stack.nl/~dimitri/doxygen/>`__.

.. code:: bash

    # in esphomedocs repo:
    pip3 install -r requirements.txt

.. note::

    Alternatively, you can use the `esphomedocs docker image <https://hub.docker.com/r/ottowinter/esphomedocs/>`__:

    .. code:: bash

        docker run --rm -v "$PWD/..":/data -p 8000:8000 -it ottowinter/esphomedocs

    And then go to ``<CONTAINER_IP>:8000`` in your browser.

Next, you will also need to clone the `esphomelib repository <https://github.com/OttoWinter/esphomelib>`__ into
the folder where ``esphomedocs`` sits like this:

.. code::

    ├── esphomedocs/
    │   ├── api/
    │   ├── esphomeyaml/
    │   ├── Doxygen
    │   ├── Makefile
    │   ├── index.rst
    │   └── ...
    └── esphomelib/
        ├── src/
        ├── examples/
        ├── library.json
        ├── platformio.ini
        └── ...

Then, use the provided Makefile to build the changes and start a simple web server:

.. code:: bash

    # Update doxygen API docs
    make doxyg
    # Start web server on port 8000
    make webserver

    # Updates then happen via:
    make html

Some notes about the docs:

* Use the english language (duh...)
* An image tells a thousand words, please use them wherever possible. But also don't forget to shrink them, for example
  I often use https://tinypng.com/
* Try to use examples as often as possible (also while it's great to use highly accurate,
  and domain-specific lingo, it should not interfere with new users understanding the content)
* When adding new files, please also add them to the ``index.rst`` file in the directory you're editing.
* Fixes/improvements for the docs themselves should go to the ``current`` branch of the
  esphomedocs repository. New features should be added against the ``next`` branch.

Contributing to esphomelib
--------------------------

esphomelib is the engine behind all the esphomeyaml stuff. The framework is also designed
to be used on its own - i.e. without esphomeyaml. To contribute code to esphomelib to fix
a bug or add a new integration/feature, clone the repository, make your changes and create
a pull request.

At some point, I will create a dedicated guide for the exact setup used, but for now just
look around the code base a bit and see how other components are doing stuff.

To initialize the development environment, navigate to the repository and execute:

.. code:: bash

    # View available IDEs:
    pio init --help
    # Initialize for IDE
    pio init --ide {YOUR_IDE}

Standard for the esphomelib codebase:

- All features should at least have a bit of documentation using the doxygen documentation style
  (see other source files for reference)
- The code style is based on the `Google C++ Style Guide <https://google.github.io/styleguide/cppguide.html>`__ with
  a few modifications:

  - function, method and variable names are ``lower_snake_case``
  - class/struct/enum names should be ``UpperCamelCase``
  - constants should be ``UPPER_SNAKE_CASE``
  - fields should be ``protected`` and ``lowe_snake_case_with_trailing_underscore_``.
  - It's preferred to use long variable/function names over short and non-descriptive ones.

- Use two spaces, not tabs.
- Using ``#define`` s is discouraged and should be replaced by constants.
- Use ``using type_t = int;`` instead of ``typedef int type_t;``
- Be careful with including large standard library headers, they can considerably
  increase the code size.
- All features should only be compiled if a user explicitly defined so using ``-DUSE_<FEATURE>``
  (see ``esphomeyaml/defines.h``)
- Header files ``.h`` should not include source code. All code should sit in C++ ``.cpp`` files.
  (except for templates)
- Using explicit int sizes is like ``int64_t`` is preferred over standard types like ``long long``.
- All new features should have at least one example usage in the examples directory.
- New components should dump their configuration using ``ESP_LOGCONFIG`` at startup in ``setup()``
- The number of external libraries should be kept to a minimum. If the component you're developing has a simple
  communication interface, please consider implementing the library natively in esphomelib.
- Implementations for new devices should contain reference links for the datasheet and other sample
  implementations.
- Please test your changes :)

For editing a local copy of esphomelib within the esphomeyaml ecosystem please see
:ref:`esphomeyaml.esphomelib_version <esphomeyaml-esphomelib_version>` option.

Contributing to esphomeyaml
---------------------------

esphomeyaml primarily does two things: It validates the configuration and creates C++ code.

The configuration validation should always be very strict with validating user input - it's always
better to fail quickly if a configuration isn't right than to have the user find out the issue after
a few hours of debugging.

Preferably, the configuration validation messages should explain the exact validation issue (and not "invalid name!")
and try to suggest a possible fix.

The C++ code generation engine is 99% syntactic sugar and unfortunately not too well documented yet.
Have a look around other components and you will hopefully quickly get the gist of how to interact with
the code generation engine.

The python source code of your component will automatically be loaded if the user uses
it in the configuration. Specifically, it may contain these fields:

- ``CONFIG_SCHEMA``: for *components* like ``dallas``. This is the configuration
  schema that will be validated against the user configuration.
- ``PLATFORM_SCHEMA``: for *platforms* like ``sensor.dallas``. This is the configuration schema that
  will be validated against every ``platform:`` definition in the config of your platform name.
- ``to_code``: The "workhorse" of esphomeyaml. This will be called with the configuration of your component/platform
  and you can add code to the global code index in here.

  - Call an ``Application`` method like this ``App.make_dallas_component()``

  - Register a variable using ``variable(<TYPE>, <VAR_ID>, rhs)``. This will generate an assignment expression
    and add it to the global expression index. The return value is the left hand side variable which you can use
    for further calls.

    .. code:: cpp

        <TYPE> <VAR_ID> = <rhs>;

  - Register a variable of a pointer type using ``Pvariable(<TYPE>, <VAR_ID>, rhs)``.

    .. code:: cpp

        <TYPE> *<VAR_ID> = <rhs>;

        // rhs = App.make_dallas_component(12, 15000)
        // var = Pvariable(DallasComponent, "dallas_id", rhs)
        // add(var.hello_world())
        DallasComponent *dallas_id = App.make_dallas_component(12, 15000)
        dallas_id->hello_world()

  - Expressions like ``var.hello_world()`` are not automatically added to the code and need to be added to the
    global expression index using ``add()``.

  - Access variables using ``get_variable()``. The variable will automatically know if it is a pointer and use
    the correct operator. Additionally, you can pass a type as the second argument to ``get_variable``. This will
    cause esphomeyaml to use the first variable of that type.

    .. code:: cpp

        hub = get_variable(config.get(CONF_DALLAS_ID), DallasComponent)

  - Pass configuration arguments to mock function calls (like ``App.make_dallas_component``) using normal
    python :)

    .. code:: python

        rhs = App.make_dallas_component(config[CONF_PIN], config.get(CONF_UPDATE_INTERVAL))

    Note the ``config.get()``: Trailing ``None`` values in function calls are stripped.

- ``BUILD_FLAGS``: Pass build flags that should be provided if your component is loaded.

  .. code:: python

      BUILD_FLAGS = '-DUSE_DALLAS_SENSOR'

- ``REQUIRED_BUILD_FLAGS``: Like ``BUILD_FLAGS``, but also uses these build flags if the user has disabled build
  flags in the :doc:`esphomeyaml section </esphomeyaml/components/esphomeyaml>`.

- ``DEPENDENCIES``: Other components that are required to be in the user's configuration if this platform/component
  is loaded:

  .. code::

      DEPENDENCIES = ['i2c']

- ``ESP_PLATFORMS``: Provide a whitelist of platforms this integration works on. Default is work on all platforms.

  .. code::

      ESP_PLATFORMS = [ESP_PLATFORM_ESP32]

Run ``pip2 install -e .`` to install a development version of esphomeyaml.

See Also
--------

- :doc:`esphomeyaml index </esphomeyaml/index>`
- :doc:`faq`
- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/guides/contributing.rst>`__

.. disqus::
