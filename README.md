# proyecto de Fundamentos de Inteligencia Artificial

## descripción
Proyecto realizado para el ramo "fundamentos de Inteligencia Artificial" en la cual consiste en aplicar un algoritmo de metaehurística para resolver el problema de diseño de células de manufactura (Manufacturing Cell Design Problem o MCDP) en donde se busca minimizar el uso de células en un sistema de manufactura.
En el proyecto realizado se usó un algorítmo propuesto por E. A. Zanaty, en donde inserta el número áureo (1.618033...) a la fófmula de actualización de estado en el algotirmo de Optimización por Enjambre de Particulas o PSO. Además, este proyecto utiliza las instancias propuesto por F. F. Boctor en 1991 en su trabajo realizado sobre el tema en cuestión, para leer y realizar la tarea de optimización de este proyecto.

## Requerimientos

Python 3.6 (probado con python 3.8)

## Instrucciones de uso

1. descargar repositorio, esta incluye los archivos necesarios para leer y procesar los archivos
```bash
git clone http://github.com/dani93t/proyecto_fia
```

2. ejecutar el programa
```bash
python fia.py
```
o si Python está guardado en PATH, ejecutar
```bash
fia.py
```

### Parámetros

| parámetro | alias | descripción | valor por defecto |
| --------- | --------- | --------- | --------- |
| **-a** | **-a** | parámetro a | 1 |
| **-b** | **-b** | parámetro b | 1 |
| **-c** | **-c** | parámetro c | 1 |
| **-k** | **-k** | parámetro k | 0 |
| **--semilla** | **-s** | semilla inicial de simulación | tiempo actual |
| **--particulas** | **-p** | número de partículas de simulación | 50 |
| **--iteraciones** | **-i** | número de iteraciones de simulación | 100 |
| **--rutas** | **-r** | especifica ruta/directorio/archivos a cargar al sistema | "./BoctorProblem_90_instancias" |


## Registro de cambios
* (15-03-2021) - optimización de código.
* (23-03-2021) - implementación de parámetros y mejoras menores.
* (25-03-2021) - correcciones de código.

## Referencias
* Zanaty, E. A. (2018). A Novel Metaheuristic Algorithm based on Fibonacci Sequence. IJCSNS, 18(4), 44.
* Boctor, F. F. (1991). A Jinear formulation of the machine-part cell formation problem. The International Journal of Production Research, 29(2), 343-356.