"""
WSGI Calculator

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
application at `http://localhost:8080/multiply/3/5' then the response
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
  * Fork this repository (Session04).
  * Edit this file to meet the homework requirements.
  * Your script should be runnable using `$ python calculator.py`
  * When the script is running, I should be able to view your
    application in my browser.
  * I should also be able to see a home page (http://localhost:8080/)
    that explains how to perform calculations.
  * Commit and push your changes to your fork.
  * Submit a link to your Session04 fork repository!
"""
from functools import reduce
import operator
import traceback

def index():
    body = """
<!doctype html>
<html lang="en">
  
  <div class="container-fluid">
  
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    
  
    
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">

    <title>Dianna's Web Calculator</title>
  </head>
  <body>
    <h1>Dianna's Web Calculator</h1>
    You can use this website to add, subtract, multiply, or divide numbers.<br>
    Change the url to specify the function and numbers that you want to use.<br><br>
    Here are some examples:<br><br>

<table class="table table-hover">
  <thead>
    <tr class="table-active">
      <th scope="col">Function</th>
      <th scope="col">Numbers</th>
      <th scope="col">URL</th>
    </tr>
  </thead>
  <tbody>
    <tr class="table-success">
      <th scope="row">Add</th>
      <td>200 + 50</td>
      <td><a href=http://localhost:8080/add/200/50>http://localhost:8080/add/200/50</a></td>
    </tr>
    <tr class="table-danger">
      <th scope="row">Subtract</th>
      <td>8 - 1</td>
      <td><a href=http://localhost:8080/subtract/8/1>http://localhost:8080/subtract/8/1</a></td>
    </tr>
    <tr class="table-info">
      <th scope="row">Multiply</th>
      <td>2 * 5</td>
      <td><a href=http://localhost:8080/multiply/2/5>http://localhost:8080/multiply/2/5</a></td>
    </tr>
    <tr class="table-warning">
      <th scope="row">Divide</th>
      <td>400 / 4</td>
      <td><a href=http://localhost:8080/divide/400/4>http://localhost:8080/divide/400/4</a></td>
    </tr>
  </tbody>
</table>
    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>

    </div>

  </body>
</html>  
"""
    return body


def add(*args):
    """Returns a string with the sum of the arguments"""
    args = [int(n) for n in args]
    total = sum(args)
    return str(total)


def subtract(*args):
    """Returns a string with the difference of the arguments"""
    args = [int(n) for n in args]
    total = reduce(operator.sub, args)
    return str(total)


def multiply(*args):
    """Returns a string with the product of the arguments"""

    args = [int(n) for n in args]
    total = reduce(operator.mul, args)
    return str(total)


def divide(*args):
    """Returns a string with the quotient of the arguments"""
    args = [int(n) for n in args]
    total = reduce(operator.truediv, args)
    return str(total)


def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """

    funcs = {
        "": index,
        "add": add,
        "subtract": subtract,
        "multiply": multiply,
        "divide": divide
    }

    path = path.strip("/").split("/")

    func_name = path[0]
    args = path[1:]

    try:
        func = funcs[func_name]
    except KeyError:
        raise NameError

    return func, args

def application(environ, start_response):
    # TODO (bonus): Add error handling for a user attempting
    # to divide by zero.

    headers = [('Content-type', 'text/html')]

    try:
        path = environ.get("PATH_INFO", None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = func(*args)
        status = "200 OK"

    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"

    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
        print(traceback.format_exc())

    finally:
        headers.append(("Content-length", str(len(body))))
        start_response(status, headers)
        return [body.encode("utf8")] # Return body in byte encoding


if __name__ == '__main__':
    # Use wsgiref to make a simple server
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
