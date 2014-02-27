#!/bin/env python
"""
``GribMessage`` class that implements a GRIB message that allows access to
the message's key-value pairs in a dictionary-like manner and closes the
message when it is no longer needed, coordinating this with its host file.

Author: Daniel Lee, DWD, 2014
"""

import collections

import gribapi

class GribMessage(object):
    """
    A GRIB message.

    Each ``GribMessage`` is stored as a key/value pair in a dictionary-like
    structure. It can be used in a context manager or by itself. When the
    ``GribFile`` it belongs to is closed, it closes any open ``GribMessage``s
    that belong to it. If a ``GribMessage`` is closed before its ``GribFile``
    is closed, it informs the ``GribFile`` of its closure.

    Scalar and vector values are set appropriately through the same method.

    Usage::

        >>> with GribFile(filename) as grib:
        ...     # Access shortNames of all messages
        ...     for msg in grib:
        ...         print(msg["shortName"])
        ...     # Report number of keys in message
        ...     len(msg)
        ...     # Report message size in bytes
        ...     msg.size
        ...     # Report keys in message
        ...     msg.keys()
        ...     # Check if value is missing
        ...     msg.missing("scaleFactorOfSecondFixedSurface")
        ...     # Set scalar value
        ...     msg["scaleFactorOfSecondFixedSurface"] = 5
        ...     # Check key's value
        ...     msg["scaleFactorOfSecondFixedSurface"]
        ...     # Set value to missing
        ...     msg.set_missing("scaleFactorOfSecondFixedSurface")
        ...     # Missing values raise exception when read with dict notation
        ...     msg["scaleFactorOfSecondFixedSurface"]
        ...     # Array values are set transparently
        ...     msg["values"] = [1, 2, 3]
        ...     # Messages can be written to file
        ...     with open(testfile, "w") as test:
        ...         msg.write(test)
        ...     # Messages can be cloned from other messages
        ...     msg2 = msg.clone()
        ...     # If desired, messages can be closed manually or used in with
        ...     msg.close()
    """
    def __enter__(self):
        return self
    def __exit__(self, type, value, traceback):
        """Release GRIB message handle and inform file of release."""
        gribapi.grib_release(self.gid)
        if self.grib_file:
            self.grib_file.open_messages.remove(self)
    def close(self):
        """Possibility to manually close message."""
        self.__exit__(None, None, None)
    def __contains__(self, key):
        """Check whether a key is present in message."""
        return key in self.keys()
    def __len__(self):
        """Return key count."""
        return len(self.keys())
    def __getitem__(self, key):
        """Return value associated with key as its native type."""
        return self.get(key)
    def __setitem__(self, key, value):
        """
        Set value associated with key.

        If the object is iterable,
        """
        # Passed value is iterable and not string
        if (isinstance(value, collections.Iterable) and not
                isinstance(value, basestring)):
            gribapi.grib_set_array(self.gid, key, value)
        else:
            gribapi.grib_set(self.gid, key, value)
    def __iter__(self):
        return iter(self.keys())
    def itervalues(self):
        return self.values()
    def items(self):
        """Return list of tuples of all key/value pairs."""
        return [(key, self[key]) for key in self.keys()]
    def keys(self):
        return self.get_keys()
    def __init__(self, grib_file=None, clone=None, sample=None, index=None):
        """
        Open a message and inform the GRIB file that it's been incremented.

        If ``grib_file`` is not supplied, the message is cloned from
        ``GribMessage`` ``clone``. If neither is supplied, the ``GribMessage``
        is cloned from ``sample``.
        """
        #: Unique GRIB ID, for GRIB API interface
        self.gid = None
        #: File containing message
        self.grib_file = None
        if grib_file:
            self.gid = gribapi.grib_new_from_file(grib_file.file_handle)
            grib_file.message += 1
            self.grib_file = grib_file
        elif clone:
            self.gid = clone
        elif sample:
            self.gid = gribapi.grib_new_from_samples(sample)
        elif index:
            self.gid = gribapi.grib_new_from_index(index.iid)
        else:
            raise RuntimeError("No source was supplied "
                               "(possibilities: grib_file, clone, sample).")
        #: Size of message in bytes
        self.size = gribapi.grib_get_message_size(self.gid)
    def get_keys(self, namespace=None):
        """Get available keys in message."""
        iterator = gribapi.grib_keys_iterator_new(self.gid, namespace=namespace)
        keys = []
        while gribapi.grib_keys_iterator_next(iterator):
            key = gribapi.grib_keys_iterator_get_name(iterator)
            keys.append(key)
        gribapi.grib_keys_iterator_delete(iterator)
        return keys
    def clone(self):
        """Return clone of self."""
        return GribMessage(clone=gribapi.grib_clone(self.gid))
    def dump(self):
        """Dump message's binary content."""
        return gribapi.grib_get_message(self.gid)
    def get(self, key, type=None):
        """Get value of a given key as its native or specified type."""
        if self.missing(key):
            raise KeyError("Key is missing from message.")
        if key == "values":
            ret = gribapi.grib_get_values(self.gid)
        else:
            try:
                ret = gribapi.grib_get(self.gid, key, type)
            # This is an ugly hack because the library does not differentiate
            # exception types
            except gribapi.GribInternalError, e:
                if e.msg == "Passed array is too small":
                    ret = gribapi.grib_get_array(self.gid, key, type)
                else:
                    raise e
        return ret
    def missing(self, key):
        """Report if key is missing."""
        return bool(gribapi.grib_is_missing(self.gid, key))
    def set_missing(self, key):
        """Set a key to missing."""
        gribapi.grib_set_missing(self.gid, key)
    def write(self, outfile=None):
        """Write message to file."""
        if not outfile:
            # This is a hack because the API does not accept inheritance
            outfile = self.grib_file.file_handle
        gribapi.grib_write(self.gid, outfile)
