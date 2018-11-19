.. _time:

Time
====

.. seo::
    :description: Instructions for setting up real time clock sources in esphomelib like network based time.
    :image: clock-outline.png
    :keywords: NTP, SNTP, RTC

The ``time`` component allows you to set up real time clock time sources for esphomelib.
You can then get the current time in :ref:`lambdas <config-lambda>`.
Currently only sntp (internet-based) time is supported.

.. code-block:: yaml

    # Example configuration entry
    time:
      - platform: sntp
        id: sntp_time


Configuration variables:
------------------------

- **id** (**Required**, :ref:`config-id`): Specify the ID of the time for use in lambdas.
- **timezone** (*Optional*, string): Manually tell esphomelib what timezone to use with `this format
  <https://www.gnu.org/software/libc/manual/html_node/TZ-Variable.html>`__ (warning: the format is quite complicated).
  esphomeyaml tries to automatically infer the timezone string based on the timezone of the computer that is running
  esphomeyaml, but this might not always be accurate.
- **servers** (*Optional*, list of strings): Choose up to 3 NTP servers that are used for the clock source.
  Defaults to ``0.pool.ntp.org``, ``1.pool.ntp.org`` and ``2.pool.ntp.org``
- **on_time** (*Optional*, :ref:`Automation <automation>`): Automation to run at specific intervals using
  a cron-like syntax. See :ref:`time-on_time`.

.. note::

    To use the automatic timezone detection you will need to have the python ``tzlocal`` package installed.
    If you're running this as a HassIO add-on or with the official esphomeyaml docker image, it should already
    be installed. Otherwise you need to install it using ``pip2 install tzlocal``.

Use In Lambdas
--------------

To get the current local time with the timezone applied
in :ref:`lambdas <config-lambda>`, just call the ``.now()`` method like so:

.. code-block:: cpp

    auto time = id(sntp_time).now();

Alternatively, you can use ``.utcnow()`` to get the current UTC time.

The returned object can either be used directly to get the current minute, hour, ... as numbers or a string can be
created based on a given format. If you want to get the current time attributes, you have these fields

.. table::
    :class: no-center

    ==================== ======================================== ======================================== ====================
    **Name**             **Meaning**                              **Range (inclusive)**                    **Example**
    -------------------- ---------------------------------------- ---------------------------------------- --------------------
    ``.second``          Seconds after the minute                 [0-60] (generally [0-59],                42
                                                                  extra range is to accommodate leap
                                                                  seconds.)
    -------------------- ---------------------------------------- ---------------------------------------- --------------------
    ``.minute``          Minutes after the hour                   [0-59]                                   31
    -------------------- ---------------------------------------- ---------------------------------------- --------------------
    ``.hour``            Hours since midnight                     [0-23]                                   16
    -------------------- ---------------------------------------- ---------------------------------------- --------------------
    ``.day_of_week``     Day of the week, sunday=1                [1-7]                                    7 (saturday)
    -------------------- ---------------------------------------- ---------------------------------------- --------------------
    ``.day_of_month``    Day of the month                         [1-31]                                   18
    -------------------- ---------------------------------------- ---------------------------------------- --------------------
    ``.day_of_year``     Day of the year                          [1-366]                                  231
    -------------------- ---------------------------------------- ---------------------------------------- --------------------
    ``.month``           Month, january=1                         [1-12]                                   8 (august)
    -------------------- ---------------------------------------- ---------------------------------------- --------------------
    ``.year``            Year since 0 A.C.                        [1970-∞[                                 2018
    -------------------- ---------------------------------------- ---------------------------------------- --------------------
    ``.is_dst``          Is daylight savings time                 false, true                              true
    -------------------- ---------------------------------------- ---------------------------------------- --------------------
    ``.time``            Unix epoch time (seconds since UTC       [-2147483648 - 2147483647] (negative     1534606002
                         Midnight January 1, 1970)                values for time past January 19th 2038)
    -------------------- ---------------------------------------- ---------------------------------------- --------------------
    ``.is_valid()``      Basic check if the time is valid         false, true                              true
                         (i.e. not January 1st 1970)
    ==================== ======================================== ======================================== ====================

.. note::

    Before the ESP has connected to the internet and can get the current time the date will be January 1st 1970. So
    make sure to check if ``.is_valid()`` evaluates to ``true`` before triggering any action.


.. _strftime:

strftime
^^^^^^^^

The second way to use the time object is to directly transform it into a string like ``2018-08-16 16:31``.
This is directly done using C's `strftime <http://www.cplusplus.com/reference/ctime/strftime/>`__ function which
allows for a lot of flexibility.

.. code-block:: cpp

    # For example, in a display object
    it.strftime(0, 0, id(font), "%Y-%m-%d %H:%M", id(time).now());

The strftime will parse the format string (here ``"%Y-%m-%d %H:%M"``) and match anything beginning with
a percent sign ``%`` and a letter corresponding to one of the below formatting options and replace it
with the current time representation of that format option.

.. table::
    :class: no-center

    ============= ============================================================== =========================
    **Directive** **Meaning**                                                    **Example**
    ------------- -------------------------------------------------------------- -------------------------
    ``%a``        Abbreviated **weekday** name                                   Sat
    ------------- -------------------------------------------------------------- -------------------------
    ``%A``        Full **weekday** name                                          Saturday
    ------------- -------------------------------------------------------------- -------------------------
    ``%w``        **Weekday** as decimal number, where 0 is Sunday and 6         6
                  is Saturday
    ------------- -------------------------------------------------------------- -------------------------
    ``%d``        **Day of month** as zero-padded decimal number                 01, 02, ..., 31
    ------------- -------------------------------------------------------------- -------------------------
    ``%b``        Abbreviated **month** name                                     Aug
    ------------- -------------------------------------------------------------- -------------------------
    ``%B``        Full **month** name                                            August
    ------------- -------------------------------------------------------------- -------------------------
    ``%m``        **Month** as zero-padded decimal number                        01, 02, ..., 12
    ------------- -------------------------------------------------------------- -------------------------
    ``%y``        **Year** without century as a zero-padded decimal number       00, 01, ..., 99
    ------------- -------------------------------------------------------------- -------------------------
    ``%Y``        **Year** with century as a decimal number                      2018
    ------------- -------------------------------------------------------------- -------------------------
    ``%H``        **Hour** (24-hour clock) as a zero-padded decimal number       00, 01, ..., 23
    ------------- -------------------------------------------------------------- -------------------------
    ``%I``        **Hour** (12-hour clock) as a zero-padded decimal number       00, 01, ..., 12
    ------------- -------------------------------------------------------------- -------------------------
    ``%p``        **AM or PM** designation                                       AM, PM
    ------------- -------------------------------------------------------------- -------------------------
    ``%M``        **Minute** as a zero-padded decimal number                     00, 01, ..., 59
    ------------- -------------------------------------------------------------- -------------------------
    ``%S``        **Second** as a zero-padded decimal number                     00, 01, ..., 59
    ------------- -------------------------------------------------------------- -------------------------
    ``%j``        **Day of year** as a zero-padded decimal number                001, 002, ..., 366
    ------------- -------------------------------------------------------------- -------------------------
    ``%U``        **Week number of year** (Sunday as the first day of the week)  00, 01, ..., 53
                  as a zero-padded decimal number. All days in a new year
                  preceding the first Sunday are considered to be in week 0.
    ------------- -------------------------------------------------------------- -------------------------
    ``%W``        **Week number of year** (Monday as the first day of the week)  00, 01, ..., 53
                  as a zero-padded decimal number. All days in a new year
                  preceding the first Monday are considered to be in week 0.
    ------------- -------------------------------------------------------------- -------------------------
    ``%c``        **Date and time** representation                               Sat Aug 18 16:31:42 2018
    ------------- -------------------------------------------------------------- -------------------------
    ``%x``        **Date** representation                                        08/18/18
    ------------- -------------------------------------------------------------- -------------------------
    ``%X``        **Time** representation                                        16:31:42
    ------------- -------------------------------------------------------------- -------------------------
    ``%%``        A literal ``%`` character                                      %
    ============= ============================================================== =========================

.. _time-on_time:

``on_time``
-----------

This powerful automation can be used to run automations at specific intervals at
specific times of day. The syntax is a subset of the `crontab <https://crontab.guru/>`__ syntax.

There are two ways to specify time intervals: Either with using the ``seconds:``, ``minutes:``, ...
keys as seen below or using a cron expression like ``* /5 * * * *``.

Basically, the automation engine looks at your configured time schedule every second and
evaluates if the automation should run.

.. code-block:: yaml

    time:
      - platform: sntp
        # ...
        on_time:
          # Every 5 minutes
          - seconds: 0
            minutes: /5
            then:
              - switch.toggle: my_switch

          # Every morning on weekdays
          - seconds: 0
            minutes: 30
            hours: 7
            days_of_week: MON-FRI
            then:
              - light.turn_on: my_light

          # Cron syntax, trigger every 5 minutes
          - cron: '* /5 * * * *'
            then:
              - switch.toggle: my_switch

Configuration variables:

- **seconds** (*Optional*, string): Specify for which seconds of the minute the automation will trigger.
  Defaults to ``*`` (all seconds). Range is from 0 to 59.
- **minutes** (*Optional*, string): Specify for which minutes of the hour the automation will trigger.
  Defaults to ``*`` (all minutes). Range is from 0 to 59.
- **hours** (*Optional*, string): Specify for which hours of the day the automation will trigger.
  Defaults to ``*`` (all hours). Range is from 0 to 23.
- **days_of_month** (*Optional*, string): Specify for which days of the month the automation will trigger.
  Defaults to ``*`` (all hours). Range is from 1 to 31.
- **months** (*Optional*, string): Specify for which months of the year to trigger.
  Defaults to ``*`` (all months). The month names JAN to DEC are automatically substituted.
  Range is from 1 (January) to 12 (December).
- **days_of_week** (*Optional*, string): Specify for which days of the week to trigger.
  Defaults to ``*`` (all days). The names SUN to SAT are automatically substituted.
  Range is from 1 (Sunday) to 7 (Saturday).
- **cron** (*Optional*, string): Alternatively, you can specify a whole cron expression like
  ``* /5 * * * *``. Please note years and some special characters like ``L``, ``#`` are currently not supported.

- See :ref:`Automation <automation>`.

In the ``seconds:``, ``minutes:``, ... fields you can use the following operators:

- .. code-block:: yaml

      seconds: 0

  An integer like ``0`` or ``30`` will make the automation only trigger if the current
  second is **exactly** 0 or 30, respectively.
- .. code-block:: yaml

     seconds: 0,30,45

  You can combine multiple expressions with the ``,`` operator. This operator makes it so that
  if either one of the expressions separated by a comma holds true, the automation will trigger.
  For example ``0,30,45`` will trigger if the current second is either ``0`` or ``30`` or ``45``.
- .. code-block:: yaml

      days_of_week: 2-6
      # same as
      days_of_week: MON-FRI
      # same as
      days_of_week: 2,3,4,5,6
      # same as
      days_of_week: MON,TUE,WED,THU,FRI

  The ``-`` (hyphen) operator can be used to create a range of values and is shorthand for listing all
  values with the ``,`` operator.
- .. code-block:: yaml

      # every 5 minutes
      seconds: 0
      minutes: /5

      # every timestamp where the minute is 5,15,25,...
      seconds: 0
      minutes: 5/10

  The ``/`` operator can be used to create a step value. For example ``/5`` for ``minutes:`` makes an
  automation trigger only when the minute of the hour is 0, or 5, 10, 15, ... The value in front of the
  ``/`` specifies the offset with which the step is applied.

- .. code-block:: yaml

      # Every minute
      seconds: 0
      minutes: '*'

  Lastly, the ``*`` operator matches every number. In the example above, ``*`` could for example be substituted
  with  ``0-59``.


.. warning::

    Please note the following automation would trigger for each second in the minutes 0,5,10,15 and not
    once per 5 minutes as the seconds variable is not set:

    .. code-block:: yaml

        time:
          - platform: sntp
            # ...
            on_time:
              - minutes: /5
                then:
                  - switch.toggle: my_switch


See Also
--------

- :doc:`API Reference </api/core/time>`
- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/components/time.rst>`__

.. disqus::
