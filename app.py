import logging

from spyne import ServiceBase
from spyne.model.primitive import Unicode, Integer
from spyne.model.complex import Iterable
from spyne.application import Application
from spyne.protocol.soap import Soap11, Soap12
from spyne.server.wsgi import WsgiApplication
from spyne.decorator import rpc


def on_method_return_string(ctx):
    ctx.out_string[0] = ctx.out_string[0].replace(b'tns', b'targetNamespace')


class HelloWorldService(ServiceBase):

    @rpc(Unicode, Integer, _returns=Iterable(Unicode),
         _in_message_name='create',
         _out_message_name='created',
         _out_variable_name='created')
    def say_hello(ctx, name, times):
        for i in range(times):
            yield 'Hello, %s' % name


HelloWorldService.event_manager.add_listener('method_return_string',
                                             on_method_return_string)

application = Application([HelloWorldService],
                          tns='targetNamespace',
                          in_protocol=Soap12(validator='lxml'),
                          out_protocol=Soap12())


if __name__ == '__main__':
    # You can use any Wsgi server. Here, we chose
    # Python's built-in wsgi server but you're not
    # supposed to use it in production.
    from wsgiref.simple_server import make_server
    logging.basicConfig(level=logging.INFO)
    logging.getLogger('spyne.protocol.xml').setLevel(logging.DEBUG)
    wsgi_app = WsgiApplication(application)
    server = make_server('0.0.0.0', 8000, wsgi_app)
    server.serve_forever()
