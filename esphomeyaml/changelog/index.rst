Changelog - Version 1.9.0
=========================

================================================== ================================================== ==================================================
|Beta Releases|_                                   |Text Sensors|_                                    |MQTT Subscribe|_
-------------------------------------------------- -------------------------------------------------- --------------------------------------------------
`Beta Releases`_                                   `Text Sensors`_                                    `MQTT Subscribe`_
-------------------------------------------------- -------------------------------------------------- --------------------------------------------------
|Stepper|_                                         |CSE7766|_                                         |PMSX003|_
-------------------------------------------------- -------------------------------------------------- --------------------------------------------------
`Stepper`_                                         `CSE7766`_                                         `PMSX003`_
================================================== ================================================== ==================================================

.. |Beta Releases| image:: /esphomeyaml/images/new-box.svg
    :class: component-image
.. _Beta Releases: /esphomeyaml/guides/faq.html#how-do-i-update-to-the-latest-beta-release.html
.. |Text Sensors| image:: /esphomeyaml/images/folder-open.svg
    :class: component-image
.. _Text Sensors: /esphomeyaml/components/text_sensor/index.html
.. |MQTT Subscribe| image:: /esphomeyaml/images/mqtt.png
    :class: component-image
.. _MQTT Subscribe: /esphomeyaml/components/sensor/mqtt_subscribe.html
.. |Stepper| image:: /esphomeyaml/images/stepper.svg
    :class: component-image
.. _Stepper: /esphomeyaml/components/stepper/index.html
.. |CSE7766| image:: /esphomeyaml/images/cse7766.svg
    :class: component-image
.. _CSE7766: /esphomeyaml/components/sensor/cse7766.html
.. |PMSX003| image:: /esphomeyaml/images/pmsx003.svg
    :class: component-image
.. _PMSX003: /esphomeyaml/components/sensor/pmsx003.html


New Components
--------------

- There's a new base component called :doc:`text sensors </esphomeyaml/components/text_sensor/index>` for using
  text-based inputs, not just numbers like the generic :doc:`sensors </esphomeyaml/components/sensor/index>` did
  (`#166 <https://github.com/OttoWinter/esphomeyaml/pull/166>`__, `#52 <https://github.com/OttoWinter/esphomedocs/pull/52>`__)

- The new MQTT Subscribe Sensors allow you to get external data into esphomelib's ecosystem via MQTT
  (`#193 <https://github.com/OttoWinter/esphomelib/pull/193>`_, `#175 <https://github.com/OttoWinter/esphomeyaml/pull/175>`__,
  `#50 <https://github.com/OttoWinter/esphomedocs/pull/50>`__)

- Added :doc:`CSE7766 Power Sensor </esphomeyaml/components/sensor/cse7766>` to support power measurements
  on the Sonoff Pow R2 (`#227 <https://github.com/OttoWinter/esphomelib/pull/227>`__, `#190 <https://github.com/OttoWinter/esphomeyaml/pull/190>`__, `#59 <https://github.com/OttoWinter/esphomedocs/pull/59>`__)

- Added the :doc:`PMSX003 Particulate Matter Sensor </esphomeyaml/components/sensor/pmsx003>`
  (`#229 <https://github.com/OttoWinter/esphomelib/pull/229>`__, `#192 <https://github.com/OttoWinter/esphomeyaml/pull/192>`__, `#58 <https://github.com/OttoWinter/esphomedocs/pull/58>`__)

- Added support for :doc:`A4988 Stepper Motors </esphomeyaml/components/stepper/index>` (`#239 <https://github.com/OttoWinter/esphomelib/pull/239>`__,
  `#206 <https://github.com/OttoWinter/esphomeyaml/pull/206>`__, `#68 <https://github.com/OttoWinter/esphomedocs/pull/68>`__)

New Features
------------

- :doc:`GPIO Switches </esphomeyaml/components/switch/gpio>` now have a ``power_on_value`` option which will
  initialize the state of the switch very early in the boot process. (`#207 <https://github.com/OttoWinter/esphomelib/pull/207>`__,
  `#55 <https://github.com/OttoWinter/esphomedocs/pull/55>`__)

- The :doc:`Over-the-Air Update </esphomeyaml/components/ota>` process was quite buggy sometimes and the Arduino-library
  esphomelib used was doing some weird stuff. The OTA-process has now been completely re-written to be more stable
  (`#204 <https://github.com/OttoWinter/esphomelib/pull/204>`__, `#177 <https://github.com/OttoWinter/esphomeyaml/pull/177>`__)

- Add support for the Home Assistant device registry. If you're using `Home Assistant 0.81.0 <https://www.home-assistant.io/blog/2018/10/26/release-81/>`__
  or higher you will see a list of all components for each esphomelib node in the integrations screen (`#233 <https://github.com/OttoWinter/esphomelib/pull/233>`__).

- The current esphomelib version and compilation time are no printed on each boot
  (`#189 <https://github.com/OttoWinter/esphomelib/pull/189>`__, `#159 <https://github.com/OttoWinter/esphomeyaml/pull/159>`__):

  .. code:: bash

    [13:57:33][I][application:092]: You're running esphomelib v1.9.0 compiled on Nov  3 2018, 13:55:11

- Stack traces in the USB logs are now automatically decoded to make debugging easier (`#214 <https://github.com/OttoWinter/esphomeyaml/pull/214>`__)

- Added :ref:`mqtt-on_json_message` and :ref:`mqtt-publish_json_action` to make using JSON for MQTT payloads easier
  (`#230 <https://github.com/OttoWinter/esphomelib/pull/230>`__, `#193 <https://github.com/OttoWinter/esphomeyaml/pull/193>`__,
  `#60 <https://github.com/OttoWinter/esphomedocs/pull/60>`__)

- The remote (IR) components have received support for Samsung's IR protocol (`#176 <https://github.com/OttoWinter/esphomeyaml/pull/176>`__,
  `#48 <https://github.com/OttoWinter/esphomedocs/pull/48>`__)

- Added :ref:`component-update_action`, :ref:`logger-log_action` and :ref:`script-execute_action` for simplifying
  automations (`#232 <https://github.com/OttoWinter/esphomelib/pull/232>`__, `#196 <https://github.com/OttoWinter/esphomeyaml/pull/196>`__,
  `#198 <https://github.com/OttoWinter/esphomeyaml/pull/198>`__, `#61 <https://github.com/OttoWinter/esphomedocs/pull/61>`__,
  `#63 <https://github.com/OttoWinter/esphomedocs/pull/63>`__)

- Added an :ref:`pn532-on_tag` to :doc:`PN532 NFC Readers </esphomeyaml/components/pn532>` so that automations
  can directly use the NFC tag ID (`#194 <https://github.com/OttoWinter/esphomelib/pull/194>`__,
  `#189 <https://github.com/OttoWinter/esphomeyaml/pull/189>`__, `#57 <https://github.com/OttoWinter/esphomedocs/pull/57>`__).

- Added a ``hass-config`` command which generates a Home Assistant configuration for your esphomeyaml nodes.
  Useful if you're not using MQTT discovery (`#208 <https://github.com/OttoWinter/esphomeyaml/pull/208>`__)

- All documentation pages now have comment systems powered by `disqus <https://disqus.com/>`__ (`#47 <https://github.com/OttoWinter/esphomedocs/pull/47>`__)

- You now have to option to have a different log level for log messages sent over MQTT (:ref:`docs <mqtt-message>`,
  `#167 <https://github.com/OttoWinter/esphomeyaml/pull/167>`__, `#51 <https://github.com/OttoWinter/esphomedocs/pull/51>`__)

- Added a color correction option to :doc:`FastLED addressable lights </esphomeyaml/components/light/fastled_clockless>`
  (`#234 <https://github.com/OttoWinter/esphomelib/pull/234>`__, `#200 <https://github.com/OttoWinter/esphomeyaml/pull/200>`__,
  `#64 <https://github.com/OttoWinter/esphomedocs/pull/64>`__)

- Added a ``clean`` command to esphomeyaml to fix some occasional build errors (`#181 <https://github.com/OttoWinter/esphomeyaml/pull/181>`__)

- Added a ``send_first_at`` option to sliding window moving average sensor filters (`#240 <https://github.com/OttoWinter/esphomelib/pull/240>`__,
  `#207 <https://github.com/OttoWinter/esphomeyaml/pull/207>`__, `#69 <https://github.com/OttoWinter/esphomedocs/pull/69>`__)


Breaking Changes
----------------

- As part of the rewrite of Over-The-Air updates, the old OTA protocol is incompatible with the new one -
  But fear not, esphomeyaml still supports the legacy OTA update process. On your first OTA upload with 1.9.0, you will
  see esphomeyaml try with the new OTA method and fail. After that, esphomeyaml will fall back to the old OTA
  process and upload correctly (`#204 <https://github.com/OttoWinter/esphomelib/pull/204>`__).

- esphomelib's naming convention has been made more consistent. If you're not using any :ref:`lambdas <config-lambda>`,
  everything will still work. However, if you're using the C++ API, there are a couple of breaking changes:

  For sensors and binary sensors, ``id(my_sensor).value`` has been deprecated and ``id(my_sensor).state`` should be used
  instead. Additionally, the syntax for toggling lights and switches through C++ has been changed. Please see
  the `esphomedocs (#62) <https://github.com/OttoWinter/esphomedocs/pull/62>`__ changeset for more information
  (`#231 <https://github.com/OttoWinter/esphomelib/pull/231>`__,  `#62 <https://github.com/OttoWinter/esphomedocs/pull/62>`__,
  `#197 <https://github.com/OttoWinter/esphomeyaml/pull/197>`__)

All changes
-----------

- esphomedocs: Clarify ESP32 BLE Tracker comment `#42 <https://github.com/OttoWinter/esphomedocs/pull/42>`__
- esphomeyaml: Add a link to Home Assistant in README `#152 <https://github.com/OttoWinter/esphomeyaml/pull/152>`__ by `@jonnyair <https://github.com/jonnyair>`__
- esphomelib: Add a link to Home Assistant in README.md `#184 <https://github.com/OttoWinter/esphomelib/pull/184>`__ by `@jonnyair <https://github.com/jonnyair>`__
- esphomedocs: Fix time docs 12-hour clock strftime format `#43 <https://github.com/OttoWinter/esphomedocs/pull/43>`__
- esphomelib: Fix ESP32 BLE Presence detection always on `#185 <https://github.com/OttoWinter/esphomelib/pull/185>`__
- esphomelib: Fix LCD display include `#186 <https://github.com/OttoWinter/esphomelib/pull/186>`__
- esphomelib: Fix template switch spamming output `#187 <https://github.com/OttoWinter/esphomelib/pull/187>`__
- esphomelib: Fix using HTU21D for SI7021 `#188 <https://github.com/OttoWinter/esphomelib/pull/188>`__
- esphomelib: Fix components sending invalid state on startup if integration not ready yet `#195 <https://github.com/OttoWinter/esphomelib/pull/195>`__
- esphomelib: Log esphomelib version and compilation time on boot `#189 <https://github.com/OttoWinter/esphomelib/pull/189>`__ (new-feature)
- esphomeyaml: Log esphomelib version and compilation time on boot `#159 <https://github.com/OttoWinter/esphomeyaml/pull/159>`__ (new-feature)
- esphomeyaml: Fix raw remote receiver `#158 <https://github.com/OttoWinter/esphomeyaml/pull/158>`__
- esphomelib: Add Code of Conduct (Contributor Covenant) `#196 <https://github.com/OttoWinter/esphomelib/pull/196>`__
- esphomelib: Create CONTRIBUTING.md `#197 <https://github.com/OttoWinter/esphomelib/pull/197>`__
- esphomelib: Create issue templates `#198 <https://github.com/OttoWinter/esphomelib/pull/198>`__
- esphomelib: Create pull request template `#199 <https://github.com/OttoWinter/esphomelib/pull/199>`__
- esphomeyaml: Create Pull Request Template `#172 <https://github.com/OttoWinter/esphomeyaml/pull/172>`__
- esphomeyaml: Create CONTRIBUTING.md `#169 <https://github.com/OttoWinter/esphomeyaml/pull/169>`__
- esphomeyaml: Add Code of Conduct (Contributor Covenant) `#168 <https://github.com/OttoWinter/esphomeyaml/pull/168>`__
- esphomeyaml: Create issue templates `#171 <https://github.com/OttoWinter/esphomeyaml/pull/171>`__
- esphomedocs: Add Code of Conduct (Contributor Covenant) `#44 <https://github.com/OttoWinter/esphomedocs/pull/44>`__
- esphomedocs: Create Pull Request Template `#45 <https://github.com/OttoWinter/esphomedocs/pull/45>`__
- esphomeyaml: Fix readme broken link `#174 <https://github.com/OttoWinter/esphomeyaml/pull/174>`__
- esphomelib: Fix pulse counter counting inverted on ESP8266 `#200 <https://github.com/OttoWinter/esphomelib/pull/200>`__
- esphomeyaml: Add use_build_flags removal notice `#173 <https://github.com/OttoWinter/esphomeyaml/pull/173>`__
- esphomedocs: Highlight update_interval gotchas `#46 <https://github.com/OttoWinter/esphomedocs/pull/46>`__
- esphomedocs: Add Disqus and cleanup `#47 <https://github.com/OttoWinter/esphomedocs/pull/47>`__ (new-feature)
- esphomelib: Fix PN532 not logging discovered tags `#202 <https://github.com/OttoWinter/esphomelib/pull/202>`__
- esphomeyaml: Add Samsung IR protocol `#176 <https://github.com/OttoWinter/esphomeyaml/pull/176>`__ by `@escoand <https://github.com/escoand>`__ (new-feature)
- esphomedocs: add samsung ir protocol `#48 <https://github.com/OttoWinter/esphomedocs/pull/48>`__ by `@escoand <https://github.com/escoand>`__ (new-feature)
- esphomelib: Bump FastLED to 3.2.0 `#203 <https://github.com/OttoWinter/esphomelib/pull/203>`__
- esphomeyaml: Fix Wifi power_save_mode option `#178 <https://github.com/OttoWinter/esphomeyaml/pull/178>`__
- esphomelib: Fix application sort order `#211 <https://github.com/OttoWinter/esphomelib/pull/211>`__
- esphomedocs: Improve pulse counter docs `#49 <https://github.com/OttoWinter/esphomedocs/pull/49>`__
- esphomelib: Fix ESP32 BLE Controller Init `#213 <https://github.com/OttoWinter/esphomelib/pull/213>`__
- esphomelib: Fix Web Server Creating Infinite Print Loop `#214 <https://github.com/OttoWinter/esphomelib/pull/214>`__
- esphomelib: Add TOGGLE payload to more components `#212 <https://github.com/OttoWinter/esphomelib/pull/212>`__ (new-feature)
- esphomelib: ESP8266 Pulse Counter Improve Timing `#205 <https://github.com/OttoWinter/esphomelib/pull/205>`__
- esphomelib: Add MQTT Subscribe Sensor `#193 <https://github.com/OttoWinter/esphomelib/pull/193>`__ (new-feature)
- esphomedocs: Add MQTT Subscribe sensor `#50 <https://github.com/OttoWinter/esphomedocs/pull/50>`__ (new-feature)
- esphomeyaml: Add MQTT Subscribe sensor `#175 <https://github.com/OttoWinter/esphomeyaml/pull/175>`__ (new-feature)
- esphomeyaml: MQTT different log level `#167 <https://github.com/OttoWinter/esphomeyaml/pull/167>`__ (new-feature)
- esphomedocs: Add option to have different log level over MQTT `#51 <https://github.com/OttoWinter/esphomedocs/pull/51>`__ (new-feature)
- esphomeyaml: Add clean build files command and auto-clean on version change `#181 <https://github.com/OttoWinter/esphomeyaml/pull/181>`__ (new-feature)
- esphomelib: Add power on value to switch `#207 <https://github.com/OttoWinter/esphomelib/pull/207>`__ (new-feature)
- esphomelib: Rework OTA to be more stable `#204 <https://github.com/OttoWinter/esphomelib/pull/204>`__ (breaking-change) (new-feature)
- esphomeyaml: Rework OTA to be more stable `#177 <https://github.com/OttoWinter/esphomeyaml/pull/177>`__ (new-feature)
- esphomelib: Fix WiFi not working when GPIO 0 connected `#215 <https://github.com/OttoWinter/esphomelib/pull/215>`__
- esphomelib: Fix MiFlora illuminance reading `#220 <https://github.com/OttoWinter/esphomelib/pull/220>`__
- esphomelib: Remove invalid file headers `#219 <https://github.com/OttoWinter/esphomelib/pull/219>`__
- esphomeyaml: Fix config dump time output `#184 <https://github.com/OttoWinter/esphomeyaml/pull/184>`__
- esphomelib: GPIO Switch Rewrite `#217 <https://github.com/OttoWinter/esphomelib/pull/217>`__
- esphomedocs: Add power on value to GPIO Switch `#55 <https://github.com/OttoWinter/esphomedocs/pull/55>`__ (new-feature)
- esphomeyaml: GPIO Switch Power On Value v2 `#183 <https://github.com/OttoWinter/esphomeyaml/pull/183>`__
- esphomeyaml: Decentralize Automation Generator Code `#182 <https://github.com/OttoWinter/esphomeyaml/pull/182>`__
- esphomelib: Add PN532 On Tag Trigger `#226 <https://github.com/OttoWinter/esphomelib/pull/226>`__ (new-feature)
- esphomelib: Add text sensors `#194 <https://github.com/OttoWinter/esphomelib/pull/194>`__ (new-feature)
- esphomedocs: Add Text sensors `#52 <https://github.com/OttoWinter/esphomedocs/pull/52>`__ (new-feature)
- esphomelib: Fix PCF8574 assert. `#223 <https://github.com/OttoWinter/esphomelib/pull/223>`__ by `@lobradov <https://github.com/lobradov>`__
- esphomelib: Unify Xiaomi MiJia&MiFlora Implementations `#225 <https://github.com/OttoWinter/esphomelib/pull/225>`__
- esphomedocs: Unify xiaomi implementations `#56 <https://github.com/OttoWinter/esphomedocs/pull/56>`__
- esphomeyaml: Unify Xiaomi implementations `#188 <https://github.com/OttoWinter/esphomeyaml/pull/188>`__
- esphomelib: Add CSE7766 for Sonoff Pow R2 `#227 <https://github.com/OttoWinter/esphomelib/pull/227>`__ (new-feature)
- esphomedocs: Add CSE7766 for Sonoff Pow R2 `#59 <https://github.com/OttoWinter/esphomedocs/pull/59>`__ (new-feature)
- esphomedocs: Add PN532 On Tag Trigger `#57 <https://github.com/OttoWinter/esphomedocs/pull/57>`__ (new-feature)
- esphomeyaml: Add CSE776 for Sonoff Pow R2 `#190 <https://github.com/OttoWinter/esphomeyaml/pull/190>`__ (new-feature)
- esphomeyaml: Add Text Sensors `#166 <https://github.com/OttoWinter/esphomeyaml/pull/166>`__ (new-feature)
- esphomeyaml: Add PN532 On Tag Trigger `#189 <https://github.com/OttoWinter/esphomeyaml/pull/189>`__ (new-feature)
- esphomelib: Add MQTT publish JSON action and subscribe JSON trigger `#230 <https://github.com/OttoWinter/esphomelib/pull/230>`__ (new-feature)
- esphomeyaml: Add MQTT publish JSON action and subscribe JSON trigger `#193 <https://github.com/OttoWinter/esphomeyaml/pull/193>`__ (new-feature)
- esphomedocs: Add MQTT publish JSON action and subscribe JSON trigger `#60 <https://github.com/OttoWinter/esphomedocs/pull/60>`__ (new-feature)
- esphomelib: Add PMSX003 Particulate Matter Sensor `#229 <https://github.com/OttoWinter/esphomelib/pull/229>`__ (new-feature)
- esphomedocs: Add PMSX003 Particulate Matter Sensor `#58 <https://github.com/OttoWinter/esphomedocs/pull/58>`__ (new-feature)
- esphomelib: Add update component action and scripts `#232 <https://github.com/OttoWinter/esphomelib/pull/232>`__ (new-feature)
- esphomedocs: Add update component action and scripts `#61 <https://github.com/OttoWinter/esphomedocs/pull/61>`__ (new-feature)
- esphomelib: Implement HASS device registry for MQTT components `#233 <https://github.com/OttoWinter/esphomelib/pull/233>`__ (new-feature)
- esphomelib: Add FastLED color correction option `#234 <https://github.com/OttoWinter/esphomelib/pull/234>`__ (new-feature)
- esphomedocs: Add FastLED color correction option `#64 <https://github.com/OttoWinter/esphomedocs/pull/64>`__ (new-feature)
- esphomeyaml: Add update component action and scripts `#196 <https://github.com/OttoWinter/esphomeyaml/pull/196>`__ (new-feature)
- esphomeyaml: Add PMSX003 Particulate Matter Sensor `#192 <https://github.com/OttoWinter/esphomeyaml/pull/192>`__ (new-feature)
- esphomeyaml: Add FastLED color correction option `#200 <https://github.com/OttoWinter/esphomeyaml/pull/200>`__ (new-feature)
- esphomeyaml: Fix triggers being interpreted as a sequence of automations `#199 <https://github.com/OttoWinter/esphomeyaml/pull/199>`__
- esphomeyaml: Fix value range trigger :expressionless: `#201 <https://github.com/OttoWinter/esphomeyaml/pull/201>`__
- esphomelib: Make naming convention consistent `#231 <https://github.com/OttoWinter/esphomelib/pull/231>`__ (breaking-change)
- esphomedocs: Make naming convention consistent `#62 <https://github.com/OttoWinter/esphomedocs/pull/62>`__ (breaking-change)
- esphomedocs: Fix some typos `#65 <https://github.com/OttoWinter/esphomedocs/pull/65>`__
- esphomeyaml: Improve API naming convention consistency `#197 <https://github.com/OttoWinter/esphomeyaml/pull/197>`__ (breaking-change)
- esphomeyaml: Fix some typos `#202 <https://github.com/OttoWinter/esphomeyaml/pull/202>`__
- esphomedocs: Add logger.log action `#63 <https://github.com/OttoWinter/esphomedocs/pull/63>`__ (new-feature)
- esphomeyaml: Add logger.log action `#198 <https://github.com/OttoWinter/esphomeyaml/pull/198>`__ (new-feature)
- esphomedocs: Fix template sensor docs `#66 <https://github.com/OttoWinter/esphomedocs/pull/66>`__
- esphomedocs: Fix text sensor outdated API docs `#70 <https://github.com/OttoWinter/esphomedocs/pull/70>`__
- esphomedocs: Add Stepper Support `#68 <https://github.com/OttoWinter/esphomedocs/pull/68>`__ (new-feature)
- esphomelib: Add stepper motor support `#239 <https://github.com/OttoWinter/esphomelib/pull/239>`__ (new-feature)
- esphomelib: Add send_first_at option to sliding window sensor filter `#240 <https://github.com/OttoWinter/esphomelib/pull/240>`__ (new-feature)
- esphomedocs: Add send_first_at option to sliding window sensor filter `#69 <https://github.com/OttoWinter/esphomedocs/pull/69>`__ (new-feature)
- esphomelib: Fix display line drawing algorithm `#241 <https://github.com/OttoWinter/esphomelib/pull/241>`__
- esphomelib: Fix availability calculation `#242 <https://github.com/OttoWinter/esphomelib/pull/242>`__
- esphomeyaml: Add Stepper Motor Support `#206 <https://github.com/OttoWinter/esphomeyaml/pull/206>`__ (new-feature)
- esphomeyaml: Add send_first_at option to sliding window sensor filter `#207 <https://github.com/OttoWinter/esphomeyaml/pull/207>`__ (new-feature)
- esphomedocs: Switch example to Dehumidifier, minor grammar/puncuation `#67 <https://github.com/OttoWinter/esphomedocs/pull/67>`__ by `@rorpage <https://github.com/rorpage>`__
- esphomeyaml: Auto-Decode stacktraces `#214 <https://github.com/OttoWinter/esphomeyaml/pull/214>`__ (new-feature)
- esphomeyaml: Add generate home assistant config command `#208 <https://github.com/OttoWinter/esphomeyaml/pull/208>`__ (new-feature)

Past Changelogs
---------------

.. toctree::
    :glob:
    :maxdepth: 1

    *

.. disqus::
