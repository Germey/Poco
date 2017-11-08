# -*- coding: utf-8 -*-
# @Author: gzliuxin
# @Email:  gzliuxin@corp.netease.com
# @Date:   2017-07-14 19:47:51
from poco import Poco
from poco.agent import PocoAgent
from poco.freezeui.hierarchy import FreezedUIHierarchy, FreezedUIDumper
from poco.utils.airtest import AirtestInput, AirtestScreen
from poco.utils.simplerpc.rpcclient import RpcClient
from poco.utils.simplerpc.transport.tcp.main import TcpClient
from poco.utils.simplerpc.utils import sync_wrapper

DEFAULT_ADDR = ("localhost", 5001)


class UnityPocoAgent(PocoAgent):

    def __init__(self, addr=DEFAULT_ADDR, unity_editor=False):
        if not unity_editor:
            # init airtest env
            from poco.utils.airtest import connect_device, airtest_device
            if not airtest_device():
                connect_device("Android:///")
            # unity games poco sdk listens on Android localhost:5001
            airtest_device().adb.forward("tcp:%s" % addr[1], "tcp:5001", False)

        self.conn = TcpClient(addr)
        self.c = RpcClient(self.conn)
        self.c.DEBUG = False
        self.c.run(backend=True)
        self.c.wait_connected()

        hierarchy = FreezedUIHierarchy(Dumper(self.c))
        screen = AirtestScreen()
        input = AirtestInput()
        super(UnityPocoAgent, self).__init__(hierarchy, input, screen, None)


class Dumper(FreezedUIDumper):

    def __init__(self, rpcclient):
        super(Dumper, self).__init__()
        self.rpcclient = rpcclient

    @sync_wrapper
    def dumpHierarchy(self):
        return self.rpcclient.call("Dump")


class UnityPoco(Poco):

    def __init__(self, addr=DEFAULT_ADDR, unity_editor=False):
        agent = UnityPocoAgent(addr, unity_editor)
        super(UnityPoco, self).__init__(agent, action_interval=0.01)

    def on_pre_action(self, action, proxy, args):
        # airteset log用
        from airtest.core.main import snapshot
        snapshot(msg=unicode(proxy))

