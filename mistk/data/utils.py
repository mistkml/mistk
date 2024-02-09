##############################################################################
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
##############################################################################

import datetime
import typing

from connexion.apps.flask_app import FlaskJSONEncoder
import six

import mistk.data
from mistk import logger
import json, inspect
import re

NATIVE_TYPES_MAPPING = {
    'int': int,
    'long': int,
    'float': float,
    'str': str,
    'bool': bool,
    'date': datetime.date,
    'datetime': datetime.datetime,
    'object': object,
}


class PresumptiveJSONEncoder(FlaskJSONEncoder):
    """
    A custom JSON encoder for Data objects
    """
    include_nulls = False

    def default(self, o):  #pylint: disable=method-hidden
        """
        Defines the encoder for the object provided
        
        :param o: The object to create an encoder for
        """
        if hasattr(o, 'swagger_types') and hasattr(o, 'attribute_map'):
            dikt = {}
            for attr, _ in six.iteritems(o.swagger_types):
                value = getattr(o, attr)
                if value is None and not self.include_nulls:
                    continue
                attr = o.attribute_map[attr]
                dikt[attr] = value
            return dikt
        return FlaskJSONEncoder.default(self, o)

def serialize_model(data):
    """
    Encodes an SML object back into JSON serializable form.
    """
    return json.loads(PresumptiveJSONEncoder().encode(data))

def deserialize_model(data, klass):
    """
    Deserializes list or dict to model.

    :param data: dict, list.
    :type data: dict | list
    :param klass: class literal.
    :return: model object.
    """
    if not klass.swagger_types:
        # server object
        instance = klass()
        if not instance.swagger_types:
            return data
        attribute_map = instance.attribute_map
        swagger_types = instance.swagger_types
    else:
        # client object
        attribute_map = klass.attribute_map
        swagger_types = klass.swagger_types

    kwargs = {}
    for attr, attr_type in six.iteritems(swagger_types):
        if data is not None \
                and attribute_map[attr] in data \
                and isinstance(data, (list, dict)):
            value = data[attribute_map[attr]]
            if type(attr_type) == str:
                # client objects use strings
                kwargs[attr] = _deserialize(value, attr_type, inspect.getmodule(klass))
            else:
                kwargs[attr] = _deserialize(value, attr_type)

    instance = klass(**kwargs)

    # TODO handle alternate module name
    if isinstance(instance, mistk.data.ObjectReference):
        if instance.instance and instance.kind:
            assert hasattr(mistk.data, instance.kind), \
            "ObjectReference has invalid kind value: " + instance.kind
            klass2 = getattr(mistk.data, instance.kind)
            instance.instance = deserialize_model(instance.instance, klass2)
        elif instance.instance and not instance.kind:
            msg = "Instance given in object reference but kind attribute not specified"
            logger.error(msg + '\n%s' % instance)
            raise RuntimeError(msg)
            
    if hasattr(instance, 'object_info'):
        instance.object_info = instance.object_info or mistk.data.ObjectInfo()
        instance.object_info.kind = klass.__name__

    return instance
            

def _deserialize(data, klass, module=None):
    """
    Deserializes dict, list, str into an object.

    :param data: dict, list or str.
    :param klass: class literal, or string of class name.

    :return: object.
    """
    if data is None:
        return None
    
    if type(klass) == str:
        if klass.startswith('list['):
            sub_kls = re.match('list\[(.*)\]', klass).group(1)
            return [_deserialize(sub_data, sub_kls)
                    for sub_data in data]

        if klass.startswith('dict('):
            sub_kls = re.match('dict\(([^,]*), (.*)\)', klass).group(2)
            return {k: _deserialize(v, sub_kls)
                    for k, v in six.iteritems(data)}

        # convert str to class
        if klass in NATIVE_TYPES_MAPPING:
            klass = NATIVE_TYPES_MAPPING[klass]
        else:
            klass = getattr(module, klass)

    if klass in six.integer_types or klass in (float, str, bool):
        return _deserialize_primitive(data, klass)
    elif klass == object:
        return _deserialize_object(data)
    elif klass == datetime.date:
        return _deserialize_date(data)
    elif klass == datetime.datetime:
        return _deserialize_datetime(data)
    elif hasattr(klass, '__origin__'):
        if klass.__origin__ == list or klass.__origin__ == typing.List:
            return _deserialize_list(data, klass.__args__[0])
        if klass.__origin__ == dict or klass.__origin__ == typing.Dict:
            return _deserialize_dict(data, klass.__args__[1])
    else:
        return deserialize_model(data, klass)


def _deserialize_primitive(data, klass):
    """
    Deserializes to primitive type.

    :param data: data to deserialize.
    :param klass: class literal.

    :return: int, long, float, str, bool.
    :rtype: int | long | float | str | bool
    """
    try:
        value = klass(data)
    except UnicodeEncodeError:
        value = six.u(data)
    except TypeError:
        value = data
    return value


def _deserialize_object(value):
    """
    Return a original value.

    :return: object.
    """
    return value

def _deserialize_date(string):
    """
    Deserializes string to date.

    :param string: str.
    :type string: str
    :return: date.
    :rtype: date
    """
    try:
        from dateutil.parser import parse
        return parse(string).date()
    except ImportError:
        return string


def _deserialize_datetime(string):
    """
    Deserializes string to datetime.
    The string should be in iso8601 datetime format.

    :param string: str.
    :type string: str
    :return: datetime.
    :rtype: datetime
    """
    try:
        from dateutil.parser import parse
        return parse(string)
    except ImportError:
        return string

def _deserialize_list(data, boxed_type):
    """
    Deserializes a list and its elements.

    :param data: list to deserialize.
    :type data: list
    :param boxed_type: class literal.

    :return: deserialized list.
    :rtype: list
    """
    return [_deserialize(sub_data, boxed_type)
            for sub_data in data]


def _deserialize_dict(data, boxed_type):
    """
    Deserializes a dict and its elements.

    :param data: dict to deserialize.
    :type data: dict
    :param boxed_type: class literal.

    :return: deserialized dict.
    :rtype: dict
    """
    return {k: _deserialize(v, boxed_type)
            for k, v in six.iteritems(data)}        
        
    
def convert_client_object(obj, cls=None):
    """
    Converts an client object into the Data Model object
    
    :param obj: The object to convert
    :param cls: Defaults to None
    """
    #TODO This is pretty inefficient
    if cls:
        return deserialize_model(json.loads(PresumptiveJSONEncoder().encode(obj)), cls)
    else:
        clsname = obj.__class__.__name__
        if hasattr(mistk.data, clsname):
            cls = getattr(mistk.data, clsname)
            return deserialize_model(json.loads(PresumptiveJSONEncoder().encode(obj)), cls)
        else:
            return obj
