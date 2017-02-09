from suds.client import Client
from suds.bindings import binding


if __name__ == "__main__":
    binding.envns = ('SOAP-ENV', 'http://www.w3.org/2003/05/soap-envelope')
    hello_client = Client('http://localhost:8000/?wsdl', retxml=True)
    print(hello_client)
    print(hello_client.service.say_hello("Dave", 5))
    print(hello_client.last_received())

