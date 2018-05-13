Component
=========

.. cpp:namespace:: Component

Every object that should be handled by the Application instance and receive :cpp:func:`setup` and
:cpp:func:`loop` calls must be a subclass of :cpp:class:`Component`.

API Reference
-------------

.. cpp:namespace:: nullptr

Component
*********

.. doxygenclass:: Component
    :members:
    :protected-members:
    :undoc-members:

PollingComponent
****************

.. doxygenclass:: PollingComponent
    :members:
    :protected-members:
    :undoc-members:


Setup Priorities
****************

.. doxygennamespace:: setup_priority
