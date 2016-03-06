import yagmail
from nameko.rpc import rpc, RpcProxy


class Mail(object):
    name = "mail"

    @rpc
    def send(self, to, subject, contents):
        yag = yagmail.SMTP('myname@gmail.com', 'mypassword')
        # read the above credentials from a safe place.
        # Tip: take a look at Dynaconf setting module
        yag.send(to, subject, contents)


class Compute(object):
    name = "compute"
    mail = RpcProxy('mail')

    @rpc
    def compute(self, operation, value, other, email):
        operations = {'sum': lambda x, y: x + y,
                      'mul': lambda x, y: x * y,
                      'div': lambda x, y: x / y,
                      'sub': lambda x, y: x - y}
        try:
            result = operations[operation](value, other)
        except Exception as e:
            self.mail.send.async(email, "An error occurred", str(e))
            raise
        else:
            self.mail.send.async(
                email,
                "Your operation is complete!",
                "The result is: %s" % result
            )
            return result
