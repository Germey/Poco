# coding=utf-8
from __future__ import unicode_literals
__author__ = 'lxn3032'


class InvalidOperationException(Exception):
    """
    操作无效
    通常超出屏幕之外的点击或者滑动会判定为操作无效
    """
    pass


class PocoTargetTimeout(Exception):
    def __init__(self, action, poco_obj_proxy):
        print(repr(poco_obj_proxy))
        msg = 'Timeout when waiting for {} of "{}"'.format(action, poco_obj_proxy)
        super(PocoTargetTimeout, self).__init__(msg)


class PocoNoSuchNodeException(Exception):
    def __init__(self, objproxy):
        print(repr(objproxy))
        msg = 'Cannot find any visible node by query {}'.format(objproxy)
        super(PocoNoSuchNodeException, self).__init__(msg)


class PocoTargetRemovedException(Exception):
    def __init__(self, action, objproxy):
        print(repr(objproxy))
        msg = 'Remote ui object "{}" has been removed from hierarchy during {}.'.format(objproxy, action)
        super(PocoTargetRemovedException, self).__init__(msg)
