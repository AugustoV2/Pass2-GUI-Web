from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['POST'])
def process_request():
    data = request.json

    if 'srccode' not in data or 'optab' not in data:
        return jsonify({"error": "Missing required fields: 'srccode' and 'optab'"}), 400

    srccode = data['srccode']
    optab = data['optab']

    try:
        result = process_pass_two(srccode, optab)
        return jsonify(result), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": "An error occurred during processing. Please check your input."}), 500

def process_pass_two(srccode, optab):
    intermediate_file = []
    symtab = {}
    object_code = []

    current_address = None
    start_address = None

    for line in srccode:
        parts = line.split()
        if len(parts) == 0:
            continue

       
        if len(parts) > 1 and parts[1] == "START":
            start_address = int(parts[2])
            current_address = start_address 
            intermediate_file.append(f"{current_address:04X} - {parts[1]} {parts[2]}")
            current_address += 3  
            continue

       
        if current_address is not None:
           
            if parts[0] != '-':
                label = parts[0]
                symtab[label] = current_address  

                if len(parts) > 1:
                    opcode = parts[1]
                    if opcode in optab: 
                        object_code.append(optab[opcode])
                        intermediate_file.append(f"{current_address:04X} {label} - {opcode} {parts[2]}")
                        current_address += 3 

                    else:
                       
                        if opcode == "BYTE":
                            intermediate_file.append(f"{current_address:04X} {label} {opcode} {parts[2]}")
                            current_address += len(parts[2]) - 2  
                        elif opcode == "WORD":
                            intermediate_file.append(f"{current_address:04X} {label} {opcode} {parts[2]}")
                            current_address += 3 
                        elif opcode == "RESB":
                            intermediate_file.append(f"{current_address:04X} {label} {opcode} {parts[2]}")
                            current_address += int(parts[2]) 
                        elif opcode == "RESW":
                            intermediate_file.append(f"{current_address:04X} {label} {opcode} {parts[2]}")
                            current_address += 3 * int(parts[2])  
            else:  
                opcode = parts[1]
                if opcode in optab:
                    object_code.append(optab[opcode])
                    intermediate_file.append(f"{current_address:04X} - {opcode} {parts[2]}")
                    current_address += 3 

   
    if current_address is not None:
        intermediate_file.append(f"{current_address:04X} - END -")  

    
    object_code_output = []
    if start_address is not None and current_address is not None:
        object_code_output.append(f"H COPY {start_address:06X} {current_address:06X}") 
        object_code_output.append(f"T {start_address:06X} {' '.join(object_code)}")  
        object_code_output.append(f"E {start_address:06X}") 

    return {
        "intermediate_file": intermediate_file,
        "symtab": symtab,
        "object_code": object_code_output
    }

if __name__ == '__main__':
    app.run(debug=True)