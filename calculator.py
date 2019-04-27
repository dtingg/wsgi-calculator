"""
WSGI Calculator

Online calculator that supports addition, subtraction, multiplication, and division.
"""

from functools import reduce
import operator
import traceback


def index():
    """
    Instructions for using the calculator.
    """
    body = """
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
"""
    return body


def add(*args):
    """Returns a string with the sum of the arguments"""
    nums = map(int, args)
    total = sum(nums)

    return str(total)


def subtract(*args):
    """Returns a string with the difference of the arguments"""
    nums = map(int, args)
    total = reduce(operator.sub, nums)

    return str(total)


def multiply(*args):
    """Returns a string with the product of the arguments"""
    nums = map(int, args)
    total = reduce(operator.mul, nums)

    return str(total)


def divide(*args):
    """Returns a string with the quotient of the arguments"""
    nums = map(int, args)

    try:
        total = reduce(operator.truediv, nums)
    except ZeroDivisionError:
        raise ZeroDivisionError

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


def card_template():
    """
    Template for formatting a card.
    """
    template = """
    <div class="card">
        <div class="card-header" style="background-color:{}">
            {}
        </div>
        <div class="card-body">
            <h5 class="card-title">{}</h5><br>
            <a href="http://localhost:8080/" class="btn btn-secondary">Return home</a>
        </div>
    </div>
    """

    return template


def body_template():
    """
    Template for formatting the page
    """
    template = """
<!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
    <title>Dianna's Web Calculator</title>
  </head>
  <body>
    <div class="container-fluid">  
    <h1>Dianna's Web Calculator</h1>
    {}
    </div>
  </body>
</html>
"""
    return template


def application(environ, start_response):
    """
    Creates the response.
    """
    headers = [('Content-type', 'text/html')]

    try:
        path = environ.get("PATH_INFO", None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)

        status = "200 OK"

        if func == index:
            body = func(*args)
        else:
            body = card_template().format("#d4edda", "Success", "The answer is: {}".format(func(*args)))

    except NameError:
        status = "404 Not Found"
        body = card_template().format("#f8d7da", "Error", "Not Found")

    except ZeroDivisionError:
        status = "400 Bad Request"
        body = card_template().format("#f8d7da", "Error", "Can't divide by zero")

    except Exception:
        status = "500 Internal Server Error"
        body = card_template().format("f8d7da", "Error", "Internal Server Error")
        print(traceback.format_exc())

    finally:
        final_body = body_template().format(body)
        headers.append(("Content-length", str(len(final_body))))
        start_response(status, headers)

        return [final_body.encode("utf8")]  # Return body in byte encoding


if __name__ == '__main__':
    # Use wsgiref to make a simple server
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
