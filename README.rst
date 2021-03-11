#############
Pause on lock
#############

Automatically pause your music player when the screen gets
locked and resume plaback, once the screen is unlocked again.

This is basically `the bash script with the same name`_ rewritten in Python.
The benefit of the Python version is that it *should* detect the screensaver
you use and running player(s) automatically, as long, as they are visible on
the D-Bus. So, no need for ever growing arrays of supported applications in
the code and no configuration necessary.

Dependencies
============
The only dependency is `python-dbus-next`_ which itself has no further dependencies.

.. _the bash script with the same name: https://github.com/folixg/pause-on-lock
.. _python-dbus-next: https://github.com/altdesktop/python-dbus-next