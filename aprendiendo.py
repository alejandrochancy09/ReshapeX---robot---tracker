# Mi primer programa en Python

nombre = "Alejandro"
edad = 27
profesion = "Mechanical Engineer"

import random

edad = 27
numero = random.randint(0, 100)  # randint(1, 100) nunca da 0 — empieza en 1

resultado = edad / numero

if numero != 0:
    resultado = edad / numero
    print(f"Resultado: {resultado}")
else:
    print("No se puede dividir por cero")


print(f"Hola, me llamo {nombre}")
print(f"Tengo {edad} años")
print(f"Soy {profesion}")
print (numero)

# LISTAS — como una lista de robots
robots = ["RBT-0041", "RBT-0078", "RBT-0103", "RBT-0055"]

print("\n--- Lista de robots ---")
for robot in robots:
    print(f"Robot: {robot}")

print(f"\nTotal de robots: {len(robots)}")
print(f"Primer robot: {robots[0]}")
print(f"Último robot: {robots[-1]}")

# DICCIONARIOS — como una ficha técnica de un robot
robot = {
    "id": "RBT-0041",
    "tipo": "Welding Unit",
    "cliente": "Volcarex Auto",
    "status": "deployed",
    "progreso": 100
}

print("\n--- Ficha del robot ---")
print(f"ID: {robot['id']}")
print(f"Tipo: {robot['tipo']}")
print(f"Cliente: {robot['cliente']}")
print(f"Status: {robot['status']}")
print(f"Progreso: {robot['progreso']}%")

# Modificar un valor
robot['status'] = "maintenance"
print(f"\nNuevo status: {robot['status']}")

# FUNCIONES — código reutilizable
def verificar_robot(robot):
    if robot['progreso'] == 100:
        return "✅ Desplegado correctamente"
    elif robot['progreso'] >= 50:
        return "⚙️ En progreso"
    else:
        return "⏱️ Pendiente"

# Probar con diferentes robots
robot1 = {"id": "RBT-0041", "progreso": 100}
robot2 = {"id": "RBT-0055", "progreso": 63}
robot3 = {"id": "RBT-0090", "progreso": 20}

print("\n--- Verificación de robots ---")
print(f"{robot1['id']}: {verificar_robot(robot1)}")
print(f"{robot2['id']}: {verificar_robot(robot2)}")
print(f"{robot3['id']}: {verificar_robot(robot3)}")

# LLAMAR UNA API REAL con Python
import urllib.request
import json

url = "https://jsonplaceholder.typicode.com/users/1"
response = urllib.request.urlopen(url)
data = json.loads(response.read())

print("\n--- Datos de la API ---")
print(f"Nombre: {data['name']}")
print(f"Email: {data['email']}")
print(f"Ciudad: {data['address']['city']}")

# MANEJO DE ERRORES — try / except
print("\n--- Manejo de errores ---")

robots = ["RBT-0041", "RBT-0078", "RBT-0103"]

# Sin manejo de error — esto fallaría
# print(robots[10])  # posición 10 no existe → error

# Con manejo de error — el programa sigue funcionando
try:
    print(robots[10])        # intenta esto
except IndexError:
    print("Error: ese robot no existe en la lista")

# Otro ejemplo — división
try:
    resultado = 100 / 0
except ZeroDivisionError:
    print("Error: no se puede dividir por cero")

print("El programa siguió funcionando")

# Ejemplo simple de contador
frutas = ["manzana", "pera", "manzana", "uva", "pera", "manzana"]

conteo = {"manzana": 0, "pera": 0, "uva": 0}

for fruta in frutas:
    conteo[fruta] += 1
    print(f"Después de {fruta}: {conteo}")

print(f"\nResultado final: {conteo}")