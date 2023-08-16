from flask import Flask, jsonify, request,render_template, url_for
import math
import re

app = Flask(__name__)


@app.route('/',  methods=['GET', 'POST'])
def calculate_expression():
    if request.method == 'POST':

        expression = request.form['expression']
        variables = request.form['variables']

        if not expression or not variables:
            return render_template("calculator.html", result=None, error='Variables or Expression are not defined')

        variables_dict = {}
        for variable in variables.split(','):
            name, value = variable.split('=')
            variables_dict[name.strip()] = float(value.strip())


        try:
            result = eval_expression(expression, variables_dict)
            return render_template("calculator.html", result=str(result))

        except SyntaxError:
            return render_template("calculator.html", result=None, error='Invalid syntax')

        except NameError:
            return render_template("calculator.html", result=None, error='Unknown variable')

        except TypeError:
            return render_template("calculator.html", result=None, error='Invalid type')

        except ZeroDivisionError:
            return render_template("calculator.html", result=None, error='Division by zero')

        except ValueError as e:
            return render_template("calculator.html", result=None, error='Variables are not defined')

    return render_template("calculator.html")


def eval_expression(expression, variables):
    for var in variables:
        expression = expression.replace(var, str(variables[var]))

    expression = expression.replace('^', '**')
    expression = expression.replace('lg', 'math.log10')
    expression = expression.replace('ln', 'math.log')
    expression = expression.replace('sin', 'math.sin')
    expression = expression.replace('cos', 'math.cos')
    expression = expression.replace('tan', 'math.tan')
    expression = expression.replace('asin', 'math.asin')
    expression = expression.replace('acos', 'math.acos')
    expression = expression.replace('atan', 'math.atan')

    try:
        return eval(expression)

    except SyntaxError:
        raise SyntaxError

    except NameError:
        raise NameError

    except TypeError:
        raise TypeError

    except ZeroDivisionError:
        raise ZeroDivisionError

    except ValueError:
        raise ValueError


if __name__ == '__main__':
    app.run()