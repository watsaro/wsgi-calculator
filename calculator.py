"""
For your homework this week, you'll be creating a wsgi application of
your own.

You'll create an online calculator that can perform several operations.

You'll need to support:

  * Addition
  * Subtractions
  * Multiplication
  * Division

Your users should be able to send appropriate requests and get back
proper responses. For example, if I open a browser to your wsgi
application at `http://localhost:8080/multiple/3/5' then the response
body in my browser should be `15`.

Consider the following URL/Response body pairs as tests:

```
  http://localhost:8080/multiply/3/5   => 15
  http://localhost:8080/add/23/42      => 65
  http://localhost:8080/subtract/23/42 => -19
  http://localhost:8080/divide/22/11   => 2
  http://localhost:8080/               => <html>Here's how to use this page...</html>
```

To submit your homework:

  * Fork this repository (Session03).
  * Edit this file to meet the homework requirements.
  * Your script should be runnable using `$ python calculator.py`
  * When the script is running, I should be able to view your
    application in my browser.
  * I should also be able to see a home page (http://localhost:8080/)
    that explains how to perform calculations.
  * Commit and push your changes to your fork.
  * Submit a link to your Session03 fork repository!


"""
import traceback
from loguru import logger
import math

def add(*args):
    """ Returns a STRING with the sum of the arguments """
    sum = 0
    for arg in args:
        sum += int(arg)

    return str(sum)

# TODO: Add functions for handling more arithmetic operations.

def subtract(*args):
    """ Returns a STRING with the dif of the arguments """
    args = list(map(int, args))
    result = args[0]- args[1]

    return str(result)

def multiply(*args):
    args = list(map(int, args))
    #result = math.prod(args) does not work dont know why ERROR "AttributeError: module 'math' has no attribute 'prod'"
    result = 1
    for i in args:
        result = result * i
    return str(result)

def divided(*args):
    result = 0
    args = list(map(int, args))
    result = args[0] / args[1]
    return str(result)

def root():
    page = """
    <h1>Instructions</h1>
    <p>Choose 2 numbers to:
    <ul>
    <li>add</li>
    <li>subtract</li>
    <li>divide</li>
    <li>multiply</li>
    </ul>
    By using this format in the URL: <br/>
    hostname/action/first number/second number <br/>
    For example: <br/>
    http://localhost:8080/add/23/42 
    
    </p>

    """
    return page

def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """

    # TODO: Provide correct values for func and args. The
    # examples provide the correct *syntax*, but you should
    # determine the actual values of func and args using the
    # path.
    funcs = {
        '': root,
        'add': add,
        'subtract': subtract,
        'multiply': multiply,
        'divide': divided
    }
    path  = path.strip("/").split("/")
    func_name = path[0]

    args= path[1:]
    try:
        func = funcs[func_name]
    except KeyError:
        raise NameError

    return func, args

def application(environ, start_response):
    # TODO: Your application code from the book database
    # work here as well! Remember that your application must
    # invoke start_response(status, headers) and also return
    # the body of the response in BYTE encoding.
    headers = [('Content-type', 'text/html')]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        print(func)
        body = func(*args)

        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1> Not Found</h1>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
        print(traceback.format_exc())
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]

    # TODO (bonus): Add error handling for a user attempting
    # to divide by zero.


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
