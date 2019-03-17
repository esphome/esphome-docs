Contributing
============

.. seo::
    :description: Getting started guide for contributing to the ESPHome project
    :image: github-circle.png

Contributions to the ESPHome suite are very welcome! All the code for the projects
is hosted on GitHub and you can find the sources here:

- `ESPHome-Core <https://github.com/esphome/ESPHome-Core>`__ (The C++ framework)
- `ESPHome <https://github.com/esphome/ESPHome>`__ (The Python YAML to C++ transpiler)
- `ESPHome-Docs <https://github.com/esphome/ESPHome-Docs>`__ (The documentation which you're reading here)

Just clone the repository locally, do the changes for your new feature/bug fix and submit
a pull request. I will try to take a look at your PR as soon as possible.

Contributing to ESPHome-Docs
----------------------------

.. figure:: /images/logo-docs.svg
    :align: center
    :width: 60.0%

One of the areas of ESPHome that can always be improved is the documentation.
If you see an issue somewhere, or spelling mistakes or if you want to share your awesome
setup, please feel free to submit a pull request.

The ESPHome documentation is built using `sphinx <http://www.sphinx-doc.org/>`__ and uses
`reStructuredText <http://docutils.sourceforge.net/rst.html>`__ for all source files.

Syntax
******

In my opinion, markdown would have been the much better choice in hindsight, but at the time
I was setting up the documentation good doxygen integration was key to me. Anyway, here's a quick
RST primer:

- **Headers**: You can write titles like this:

  .. code-block:: rst

      My Title
      ========

  and section headers like this:

  .. code-block:: rst

      My Sub Section
      --------------

  and sub-section headers like this:

  .. code-block:: rst

      My Sub-sub Section
      ******************

  .. note::

      The length of the bar below the text **must** match the title Text length.
      Also, titles should be in Title Case

- **Links**: To create a link to an external resource (for example https://www.google.com), use
  ``\`Link text <link_url>\`__``. For example:

  .. code-block:: rst

      `Google.com <https://www.google.com>`__

  `Google.com <https://www.google.com>`__

- **References**: To reference another document, use the ``:doc:`` and ``:ref:`` roles (references
  are set up globally and can be used between documents):

  .. code-block:: rst

      .. _my-reference-label:

      Section to cross-reference
      ^^^^^^^^^^^^^^^^^^^^^^^^^^

      See :ref:`my-reference-label`, also see :doc:`/components/switch/gpio`.
      :doc:`Using custom text </components/switch/gpio>`.

  See :ref:`devices`, also see :doc:`/components/switch/gpio`.
  :doc:`Using custom text </components/switch/gpio>`.

- **Inline code**: To have text appear ``like this``, use double backticks:

  .. code-block:: rst

      To have text appear ``like this``, use double backticks.

  To have text appear ``like this``, use double backticks.

- **Code blocks**: To show a sample configuration file, use the ``code-block`` directive:

  .. code-block:: rst

      .. code-block:: yaml

          # Sample configuration entry
          switch:
            - platform: gpio
              name: "Relay #42"
              pin: GPIO13

  .. code-block:: yaml

      # Sample configuration entry
      switch:
        - platform: gpio
          name: "Relay #42"
          pin: GPIO13

  .. note::

      Please note the empty line after the ``code-block`` directive. That is necessary.

- **Images**: To show images, use the ``figure`` directive:

  .. code-block:: rst

      .. figure:: images/dashboard.png
          :align: center
          :width: 40.0%

          Optional figure caption.

  .. figure:: images/dashboard.png
      :align: center
      :width: 40.0%

      Optional figure caption.

  .. note::

      All images in the documentation need to be as small as possible to ensure
      fast page load times. For normal figures the maximum size should be at most
      about 1000x800px or so. Additionally, please use online tools like
      https://tinypng.com/ or https://tinyjpg.com/ to further compress images.

- **Notes and warnings**: You can create simple notes and warnings using the ``note`` and ``warning``
  directives:

  .. code-block:: rst

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

  .. code-block:: rst

      *This is italicized.* (A weird word...)
      **This is very important.**

  *This is italicized.* (A weird word...)
  **This is very important.**

- **Ordered and unordered list**: The syntax for lists in RST is more or less the same as in markdown:

  .. code-block:: rst

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

- **imgtable**: ESPHome uses a custom RST directive to show the table on the front page (see
  `index.rst <https://github.com/esphome/esphome-docs/blob/current/index.rst>`__).
  New pages need to be added to the ``imgtable`` list. The syntax is CSV with <PAGE NAME>, <FILE NAME> (without RST),
  <IMAGE> (in top-level images/ directory). The aspect ratio of these images should be 8:10 (or 10:8) but exceptions are possible.

  Because these images are served on the main page, they need to be compressed heavily. SVGs are prefered over JPGs
  and JPGs should be max. 300x300px.
  If you have imagemagick installed, you can use this command to convert the thumbnail:

  .. code-block:: bash

      convert -sampling-factor 4:2:0 -strip -interlace Plane -quality 80% -resize 300x300 in.jpg out.jpg

reStructured text can do a lot more than this, so if you're looking for a more complete guide
please have a look at the `Sphinx reStructuredText Primer <http://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html>`__.

Build
*****

.. note::

    The easiest way is to use the `esphome-docs docker image <https://hub.docker.com/r/esphome/esphome-docs/>`__:

    .. code-block:: bash

        docker run --rm -v "${PWD}/":/data -p 8000:8000 -it esphome/esphome-docs

    And then go to ``<CONTAINER_IP>:8000`` in your browser.

    This way, you don't have to install the dependencies to build the documentation.

To check your documentation changes locally, you first need install sphinx (**with Python 3**).

.. code-block:: bash

    # in ESPHome-Docs repo:
    pip3 install -r requirements.txt

Then, use the provided Makefile to build the changes and start a simple web server:

.. code-block:: bash

    # Start web server on port 8000
    make webserver

    # Updates then happen via:
    make html

Notes
*****

Some notes about the docs:

* Use the english language (duh...)
* An image tells a thousand words, please use them wherever possible. But also don't forget to shrink them, for example
  I often use https://tinypng.com/
* Try to use examples as often as possible (also while it's great to use highly accurate,
  and domain-specific lingo, it should not interfere with new users understanding the content)
* When adding new files, please also add them to the ``index.rst`` file in the directory you're editing.
* Fixes/improvements for the docs themselves should go to the ``current`` branch of the
  esphomedocs repository. New features should be added against the ``next`` branch.

Setting Up Development Environment
----------------------------------

For developing new features to ESPHome, you will first need to set up a development environment.
This is only possible for ``pip`` installs.

.. code-block:: bash

    # Clone repos
    git clone https://github.com/esphome/esphome.git
    git clone https://github.com/esphome/esphome-core.git
    git clone https://github.com/esphome/esphome-docs.git

    # Install esphome, python 2!
    cd esphome/
    pip2 install -e .
    pip2 install flake8==3.6.0 pylint==1.9.4 pillow
    # Start a new feature branch
    git checkout -b my-new-feature
    cd ..

    # Setup esphome-core environment
    cd esphome-core/
    pio init --ide vscode  # See 'pio init -h' for options
    git checkout -b my-new-feature

Now you can open esphome-core in your IDE of choice (mine is CLion) with the platformio
addons (see platformio docs for more info). Then develop the new feature with the
guidelines below.

Next, for the python part of the feature you can again use any IDE you want (I use PyCharm)
and develop the feature. You can create a ``config/`` folder inside the esphome repo
to store configs you're working with (automatically excluded by .gitignore).

To compile against your local esphome-core in esphome youhave to give the path
to the esphome core in ``esphome_core_version``:

.. code-block:: yaml

    esphome:
      esphome_core_version:
        local: path/to/esphome-core

To perform style checks for your changes (which are enforced by travis-ci) you can run

.. code-block:: bash

    flake8 esphome
    pylint esphome

Finally, for documentation changes go to your esphome-docs folder, and install sphinx (with Python 3!)

.. code-block:: bash

    pip3 install sphinx
    make webserver

Or alternatively just submit a draft PR to the docs repo and wait for netlify to create
a build preview.

Setting Up Git Environment
--------------------------

ESPHome's code-base is hosted on GitHub, and contributing is done exclusively through
"Pull Requests" (PRs) in the GitHub interface. So you need to set up your git environment
first.

When you want to create a patch for ESPHome, first go to the repository you want to contribute to
(esphome, esphome-core, etc) and click fork in the top right corner. This will create
a fork of the repository that you can modify and create git branches on.

.. code-block:: bash

    # Clone your fork
    git clone https://github.com/<YOUR_GITHUB_USERNAME>/<REPO_NAME>.git
    # For example: git clone https://github.com/OttoWinter/esphome-core.git

    # Add "upstream" remote
    git remote add upstream https://github.com/esphome/<REPO_NAME>.git
    # For example: git clone https://github.com/esphome/esphome-core.git

    # For each patch, create a new branch from latest dev
    git checkout dev
    git pull upstream dev
    git checkout -b <MY_NEW_FEATURE>
    # For example: git checkout -b gpio-switch-fix

    # Make your modifications, then commit changes with message describing changes
    git add .
    git commit -m "<COMMIT_MESSAGE>"
    # For example: git commit -m "Fix GPIO Switch Not Turning Off Interlocked Switches"

    # Upload changes
    git push -u origin <BRANCH_NAME>
    # For example: git push -u origin gpio-switch-fix

Then go to your repository fork in GitHub and wait for a create pull request message to show
up in the top (alternatively go to branches and create it from there). Fill out the
Pull Request template outlining your changes; if your PR is not ready to merge yet please
mark it as a draft PR in the dropdown of the green "create PR" button.

**Review Process:** ESPHome's code base tries to have a high code standard. At the bottom
of the Pull Request you will be able to see the "Travis" continuous integration check which
will automatically go through your patch and try to spot errors. If the CI check fails,
please see the travis log and fix all errors that appear there. Only PRs that pass the automated
checks can be merged!

**Catching up with reality**: Sometimes other commits have been made to the same files
you edited. Then your changes need to be re-applied on top of the latest changes with
a "rebase". More info `here <https://developers.home-assistant.io/docs/en/development_catching_up.html>`__.

.. code-block:: bash

    # Fetch the latest upstream changes and apply them
    git fetch upstream dev
    git rebase upstream/dev

Contributing to ESPHome-Core
----------------------------

.. figure:: /images/logo-core.svg
    :align: center
    :width: 60.0%

ESPHome-Core is the engine behind all the ESPHome stuff.
To contribute code to ESPHome-Core to fix a bug or add a new integration/feature,
clone the repository, make your changes and create a pull request.

At some point, I will create a dedicated guide for the exact setup used, but for now just
look around the code base a bit and see how other components are doing stuff.

To initialize the development environment, navigate to the repository and execute:

.. code-block:: bash

    # View available IDEs:
    pio init --help
    # Initialize for IDE
    pio init --ide {YOUR_IDE}

Standard for the esphome-core codebase:

- All features should at least have a bit of documentation using the doxygen documentation style
  (see other source files for reference)
- The code style is based on the `Google C++ Style Guide <https://google.github.io/styleguide/cppguide.html>`__ with
  a few modifications.

- function, method and variable names are ``lower_snake_case``
- class/struct/enum names should be ``UpperCamelCase``
- constants should be ``UPPER_SNAKE_CASE``
- fields should be ``protected`` and ``lowe_snake_case_with_trailing_underscore_`` (NOT private)
- It's preferred to use long variable/function names over short and non-descriptive ones.
- All uses of class members should be prefixed with ``this->`` to distinguish class from
  global functions in code review.
- Use two spaces, not tabs.
- Using ``#define`` s is discouraged and should be replaced by constants.
- Use ``using type_t = int;`` instead of ``typedef int type_t;``
- Be careful with including large standard library headers, they can considerably
  increase the code size.
- All features should only be compiled if a user explicitly defined so using ``-DUSE_<FEATURE>``
  (see ``esphome/defines.h``)
- Header files ``.h`` should not include source code. All code should sit in C++ ``.cpp`` files.
  (except for templates)
- Using explicit int sizes is like ``int64_t`` is preferred over standard types like ``long long``.
- All new features should have at least one example usage in the examples directory.
- New components should dump their configuration using ``ESP_LOGCONFIG`` at startup in ``setup()``
- The number of external libraries should be kept to a minimum. If the component you're developing has a simple
  communication interface, please consider implementing the library natively in ESPHome.
- Implementations for new devices should contain reference links for the datasheet and other sample
  implementations.
- Please test your changes :)

For editing a local copy of esphome-core within the ESPHome ecosystem please see
:ref:`esphome.esphome_core_version <esphome-esphome_core_version>` option.

Contributing to ESPHome
-----------------------

.. figure:: /images/logo-text.svg
    :align: center
    :width: 60.0%

ESPHome primarily does two things: It validates the configuration and creates C++ code.

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
- ``to_code``: The "workhorse" of ESPHome. This will be called with the configuration of your component/platform
  and you can add code to the global code index in here.

  - Call an ``Application`` method like this ``App.make_dallas_component()``

  - Register a variable using ``variable(<TYPE>, <VAR_ID>, rhs)``. This will generate an assignment expression
    and add it to the global expression index. The return value is the left hand side variable which you can use
    for further calls.

    .. code-block:: cpp

        <TYPE> <VAR_ID> = <rhs>;

  - Register a variable of a pointer type using ``Pvariable(<TYPE>, <VAR_ID>, rhs)``.

    .. code-block:: cpp

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
    cause ESPHome to use the first variable of that type.

    .. code-block:: cpp

        hub = get_variable(config.get(CONF_DALLAS_ID), DallasComponent)

  - Pass configuration arguments to mock function calls (like ``App.make_dallas_component``) using normal
    python :)

    .. code-block:: python

        rhs = App.make_dallas_component(config[CONF_PIN], config.get(CONF_UPDATE_INTERVAL))

    Note the ``config.get()``: Trailing ``None`` values in function calls are stripped.

- ``BUILD_FLAGS``: Pass build flags that should be provided if your component is loaded.

  .. code-block:: python

      BUILD_FLAGS = '-DUSE_DALLAS_SENSOR'

- ``REQUIRED_BUILD_FLAGS``: Like ``BUILD_FLAGS``, but also uses these build flags if the user has disabled build
  flags in the :doc:`esphome section </components/esphome>`.

- ``DEPENDENCIES``: Other components that are required to be in the user's configuration if this platform/component
  is loaded:

  .. code-block:: python

      DEPENDENCIES = ['i2c']

- ``ESP_PLATFORMS``: Provide a whitelist of platforms this integration works on. Default is work on all platforms.

  .. code-block:: python

      ESP_PLATFORMS = [ESP_PLATFORM_ESP32]

Run ``pip2 install -e .`` to install a development version of ESPHome.

See Also
--------

- :doc:`ESPHome index </index>`
- :doc:`faq`
- :ghedit:`Edit`

.. disqus::
