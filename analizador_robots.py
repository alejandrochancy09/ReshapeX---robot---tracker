# ANALIZADOR DE ROBOTS — proyecto completo

# Base de datos de robots
robots = [
    {"id": "RBT-0041", "tipo": "Welding Unit",     "cliente": "Volcarex Auto",   "status": "deployed",   "progreso": 100},
    {"id": "RBT-0078", "tipo": "Precision Drill",  "cliente": "Nexford Steel",   "status": "deployed",   "progreso": 100},
    {"id": "RBT-0103", "tipo": "Assembly System",  "cliente": "Orbital Dynamics","status": "deployed",   "progreso": 100},
    {"id": "RBT-0055", "tipo": "Coating Robot",    "cliente": "Lumex Corp",      "status": "inprogress", "progreso": 63},
    {"id": "RBT-0072", "tipo": "Inspection Unit",  "cliente": "Volcarex Auto",   "status": "inprogress", "progreso": 45},
    {"id": "RBT-0089", "tipo": "Welding Unit",     "cliente": "Nexford Steel",   "status": "pending",    "progreso": 0},
    {"id": "RBT-0091", "tipo": "Assembly System",  "cliente": "Lumex Corp",      "status": "pending",    "progreso": 0},
    {"id": "RBT-0095", "tipo": "Precision Drill",  "cliente": "Orbital Dynamics","status": "pending",    "progreso": 0},
]

# FUNCIÓN 1 — contar por status
def contar_por_status(robots):
    conteo = {"deployed": 0, "inprogress": 0, "pending": 0}
    for robot in robots:
        conteo[robot["status"]] += 1
    return conteo

# FUNCIÓN 2 — calcular progreso promedio
def progreso_promedio(robots):
    total = 0
    for robot in robots:
        total += robot["progreso"]
    return total / len(robots)

# FUNCIÓN 3 — filtrar por status
def filtrar_por_status(robots, status):
    resultado = []
    for robot in robots:
        if robot["status"] == status:
            resultado.append(robot)
    return resultado

# FUNCIÓN 4 — generar reporte
def generar_reporte(robots):
    conteo = contar_por_status(robots)
    promedio = progreso_promedio(robots)
    
    print("=" * 45)
    print("   REPORTE DE DESPLIEGUE — ReshapeX")
    print("=" * 45)
    print(f"Total de robots:     {len(robots)}")
    print(f"Deployed:            {conteo['deployed']}")
    print(f"En progreso:         {conteo['inprogress']}")
    print(f"Pendientes:          {conteo['pending']}")
    print(f"Progreso promedio:   {promedio:.1f}%")
    print("-" * 45)
    
    # Robots en progreso
    en_progreso = filtrar_por_status(robots, "inprogress")
    if en_progreso:
        print("\nROBOTS EN PROGRESO:")
        for r in en_progreso:
            print(f"  {r['id']} — {r['cliente']} — {r['progreso']}%")
    
    # Robots pendientes
    pendientes = filtrar_por_status(robots, "pending")
    if pendientes:
        print("\nROBOTS PENDIENTES:")
        for r in pendientes:
            print(f"  {r['id']} — {r['cliente']} — En espera")
    
    print("=" * 45)

# EJECUTAR
generar_reporte(robots)