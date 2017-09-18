# encoding=utf-8
from asyncsocket import Host, init_loop
from simplerpc import RpcBaseClient
from protocol import SimpleProtocolFilter
import json


class RpcServer(RpcBaseClient):
    """docstring for RpcServer"""
    def __init__(self):
        super(RpcServer, self).__init__()
        self.host = Host()
        self.prot = SimpleProtocolFilter()
        init_loop()

    def update(self):
        for client in self.host.remote_clients.values():
            message = client.read_message()
            if not message:
                continue
            # ！！！这里似乎有个bug，不同的client的prot混到一起了。。
            for msg in self.prot.input(message):
                message_type, result = self.handle_message(msg)
                if message_type == self.REQUEST:
                    client.say(self.prot.pack(json.dumps(result)))

        for r in self.handle_delay_result():
            # broadcast有点挫，后面在delay_result里面传client，主动send
            self.host.broadcast(self.prot.pack(json.dumps(r)))

    def call(self, cid, func, *args, **kwargs):
        req, cb = self.format_request(func, *args, **kwargs)
        msg = self.prot.pack(req)
        self.host.say(cid, msg)
        return cb


if __name__ == '__main__':
    s = RpcServer()
    # s.run()
    s.console_run({"s": s})
