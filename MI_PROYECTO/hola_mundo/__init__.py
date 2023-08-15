from flask import Flask, jsonify, request
from config import Config
from datetime import datetime
import json
from urllib.parse import unquote_plus


app = Flask(__name__)
app.config.from_object(Config)

# se carga el archivo morse_code.json
with open('morse_code.json', 'r') as morse_file:
    morse_data = json.load(morse_file)

@app.route('/')
def bienvenida():
    return 'Bienvenidx!'

@app.route('/info')
def info():
    return f'Bienvenidx a {app.config["APP_NAME"]}'

@app.route('/about')
def about():
    app_info = {
        'app_name': app.config["APP_NAME"],
        'description': app.config["APP_DESCRIPTION"],
        'developers': app.config["APP_DEVELOPERS"],
        'version': app.config["APP_VERSION"]
    }
    return jsonify(app_info)

@app.route('/sum/<int:num1>/<int:num2>')
def sum_numbers(num1, num2):
    result = num1 + num2
    return f'La suma de {num1} y {num2} es {result}'


    """
        Calculamos la edad de una persona en base a su fecha de nacimiento.

        Parametro:
            dob (str): La fecha de nacimiento en formato YYYY-MM-DD.

        Returns:
            dict: Un diccionario JSON con la edad calculada o un mensaje de error.
       
               """
@app.route('/age/<dob>')
def calculate_age(dob):
    try:
        date_of_birth = datetime.strptime(dob, '%Y-%m-%d')
        current_date = datetime.now()

        if date_of_birth > current_date:
            return jsonify({'error': 'La fecha de nacimiento no puede ser posterior a la fecha actual'})

        age = current_date.year - date_of_birth.year - ((current_date.month, current_date.day) < (date_of_birth.month, date_of_birth.day))
        return jsonify({'age': age})

    except ValueError:
        return jsonify({'error': 'Formato de fecha incorrecto. Debe ser YYYY-MM-DD'})
    
    

@app.route('/operate/<string:operation>/<int:num1>/<int:num2>')
def perform_operation(operation, num1, num2):
    
    """
    Realiza una operación matemática entre dos números enteros.

    Parametros:
        operation (str): La operación a realizar ('sum', 'sub', 'mult' o 'div').
        num1 (int): El primer número entero.
        num2 (int): El segundo número entero.

    Returns:
        dict: Un diccionario JSON con el resultado de la operación o un mensaje de error.

    
    """
    if operation == 'sum':
        result = num1 + num2
    elif operation == 'sub':
        result = num1 - num2
    elif operation == 'mult':
        result = num1 * num2
    elif operation == 'div':
        if num2 == 0:
            return jsonify({'error': 'La división no está definida para num2 igual a 0'})
        result = num1 / num2
    else:
        return jsonify({'error': 'No existe una ruta definida para ese endpoint'})

    return jsonify({'resultado': result})


@app.route('/operate')
def perform_operation_query():
    
    """
    Realiza una operación matemática entre dos números enteros utilizando parámetros de consulta (query params).

    Parametros:
        operation (str): La operación a realizar ('sum', 'sub', 'mult' o 'div') enviado como parámetro de consulta.
        num1 (int): El primer número entero enviado como parámetro de consulta.
        num2 (int): El segundo número entero enviado como parámetro de consulta.

    Returns:
        dict: Un diccionario JSON con el resultado de la operación o un mensaje de error.

    
    """
    operation = request.args.get('operation')
    num1 = int(request.args.get('num1'))
    num2 = int(request.args.get('num2'))

    if operation == 'sum':
        result = num1 + num2
    elif operation == 'sub':
        result = num1 - num2
    elif operation == 'mult':
        result = num1 * num2
    elif operation == 'div':
        if num2 == 0:
            return jsonify({'error': 'La división no está definida para num2 igual a 0'})
        result = num1 / num2
    else:
        return jsonify({'error': 'No existe una ruta definida para ese endpoint'})

    return jsonify({'resultado': result})


@app.route('/title/<string:word>')
def format_title(word):
    formatted_word = word.title()
    response = {'formatted_word': formatted_word}
    return jsonify(response)


@app.route('/formatted/<string:dni>')
def format_dni(dni):
    # Removemos caracteres no numericos 
    dni_cleaned = dni.replace('.', '').replace('-', '')

    # Verificamos que el DNI tiene exactamente 8 caracteres numéricos
    if not dni_cleaned.isdigit() or len(dni_cleaned) != 8:
        return jsonify({'error': 'El DNI no es válido'})

    formatted_dni = int(dni_cleaned)
    response = {'formatted_dni': formatted_dni}
    return jsonify(response)

@app.route('/format')
def format_user_data():
    
    """
    Formatea y procesa los datos de un usuario recibidos como parámetros de consulta (query params).

    Parametros:
        firstname (str): El nombre del usuario.
        lastname (str): El apellido del usuario.
        dob (str): La fecha de nacimiento del usuario en formato 'YYYY-MM-DD'.
        dni (str): El número de DNI del usuario.

    Returns:
        dict: Un diccionario JSON con los datos del usuario formateados y calculados.

   
    """
    firstname = request.args.get('firstname')
    lastname = request.args.get('lastname')
    dob = request.args.get('dob')
    dni = request.args.get('dni')

    
    formatted_firstname = firstname.title()
    formatted_lastname = lastname.title()

   
    dni_cleaned = dni.replace('.', '').replace('-', '')
    if not dni_cleaned.isdigit() or len(dni_cleaned) != 8:
        return jsonify({'error': 'El DNI no es válido'})
    formatted_dni = int(dni_cleaned)


    dob_date = datetime.strptime(dob, '%Y-%m-%d')
    current_date = datetime.now()
    if dob_date > current_date:
        return jsonify({'error': 'La fecha de nacimiento no puede ser posterior a la fecha actual'})
    age = current_date.year - dob_date.year - ((current_date.month, current_date.day) < (dob_date.month, dob_date.day))

    response = {
        'firstname': formatted_firstname,
        'lastname': formatted_lastname,
        'age': age,
        'dni': formatted_dni
    }
    return jsonify(response)

# Cargamos el archivo morse_code.json
with open('morse_code.json', 'r') as morse_file:
    morse_data = json.load(morse_file)
print(morse_data)  

@app.route('/encode/<string:keyword>')
def encode_to_morse(keyword):
    
    decoded_keyword = unquote_plus(keyword)
    decoded_keyword = decoded_keyword.upper()
   
    if '^' in decoded_keyword:
        return jsonify({'error': 'La palabra clave no puede contener el carácter "^"'})
    
    morse_encoded = ''
    for char in decoded_keyword:
        if char in morse_data['letters']:
            morse_encoded += morse_data['letters'][char] + '+'
        elif char.isdigit():
            morse_encoded += morse_data['letters'][char] + '+'
        elif char == ' ':
            morse_encoded += '^'  
        else:
            return jsonify({'error': 'Carácter no válido en la palabra clave'})
    
    return jsonify({'morse_encoded': morse_encoded[:-1]})  

@app.route('/decode/<string:morse_code>')
def decode_morse(morse_code):
    
    decoded_morse = morse_code.replace('%2B', '+')

    
    morse_words = decoded_morse.split('^')

    plain_text = ''
    for morse_word in morse_words:
        morse_chars = morse_word.split('+')
        decoded_word = ''
        for morse_char in morse_chars:
            if morse_char == '':  # Manejar el espacio en blanco como separador de letras
                decoded_word += ' '
            else:
                char_found = False
                for letter, code in morse_data['letters'].items():
                    if code == morse_char:
                        decoded_word += letter
                        char_found = True
                        break
                if not char_found:
                    return jsonify({'error': 'Código morse no válido'})
        plain_text += decoded_word

    return jsonify({'plain_text': plain_text})

@app.route('/convert/binary/<string:num>')
def convert_binary_to_decimal(num):
    
    if not all(digit == '0' or digit == '1' for digit in num):
        return jsonify({'error': 'Número binario no válido'})

    decimal_result = 0
    n = len(num)
    for i, digit in enumerate(num):
        power = n - 1 - i
        decimal_result += int(digit) * (2 ** power)

    return jsonify({'decimal': decimal_result})

@app.route('/balance/<string:input>')
def check_balance(input):
    stack = []
    opening_symbols = "([{"
    closing_symbols = ")]}"

    for char in input:
        if char in opening_symbols:
            stack.append(char)
        elif char in closing_symbols:
            if not stack:
                return jsonify({'balanced': False})
            last_opening_symbol = stack.pop()
            if opening_symbols.index(last_opening_symbol) != closing_symbols.index(char):
                return jsonify({'balanced': False})

    if not stack:
        return jsonify({'balanced': True})
    else:
        return jsonify({'balanced': False})