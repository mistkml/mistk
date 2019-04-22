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

"""
Module for watching a resource stored in MISTK
"""

import logging
from pubsub import pub
from queue import Queue, Empty
from mistk.data import MistkWatchEvent as WatchEvent
from mistk.data.utils import PresumptiveJSONEncoder

keepalive_time = 5
logger = logging.getLogger("WATCH")


def watch(rid, resource_version = None, init_value = None, init_value_op = "modified"):
    """
    Creates a watch on an object.
    
    :param rid: The id of the object, used to name the subscriber queue
    :param resource_version: The minimum resource version to check. 
    :param init_value: The initial value of the object to watch
    :param init_value_op: The operation to watch for. One of {created, modified, deleted}
    """
    queue = Queue()
    qid = hex(id(queue))
    ver = resource_version or 0
    logger.debug("[%s] Watching %s for versions > %s", qid, rid, ver)
    
    if init_value:
        logger.debug("[%s] Initial value of %s is %s", qid, rid, str(init_value))
        queue.put(WatchEvent(payload=init_value, event_type=init_value_op))
        
    pub.subscribe(queue.put, rid)
    
    def generator():
        try:
            logger.debug("[%s] Taking the black.", qid)
            while True:
                try:
                    event = queue.get(True, keepalive_time)
                    event_str = str(PresumptiveJSONEncoder().encode(event))
                    if hasattr(event.payload, 'object_info') and event.payload.object_info.resource_version > ver:
                        logger.debug("[%s] yielding watch event %s", qid, event_str)
                        yield event_str + "\n"
                    elif hasattr(event.payload, 'resource_version') and event.payload.resource_version > ver:
                        logger.debug("[%s] yielding watch event %s", qid, event_str)
                        yield event_str + "\n"
                    elif not hasattr(event.payload, 'object_info') and not hasattr(event.payload, 'resource_version'):
                        logger.debug("[%s] yielding watch event %s", qid, event_str)
                        yield event_str + "\n"
                    else:
                        logger.debug("[%s] watch event %s resource_version too low.  Skipping.", qid, event_str)
                except Empty:
                    logger.debug("[%s] Keepalive... this message may get annoying", qid)
                    yield ' '
                    yield ' '  # We do two of them because it takes two to recognize that the connection is closed
        finally:
            logger.debug("[%s] And now your watch has ended.", qid)
            pub.unsubscribe(queue.put, rid)
            
    return generator()
       

def notify_watch(rid, item, operation='modified'):
    """
    Notifies all subscribers of an update to a watch object
    
    :param rid: The name of the subscriber queue
    :param item: The item to send in the watch event
    :param operation: The operation that triggered this notification
    """
    logger.debug("Notification received to resource %s: %s", rid, str(item))
    pub.sendMessage(rid, item=WatchEvent(payload=item, event_type=operation))

def object_stream(objects):
    """
    Streams serialized objects as a json string
    
    :param objects: The objects to stream
    """
    for obj in objects:
        yield str(PresumptiveJSONEncoder().encode(obj)) + "\n"
        
