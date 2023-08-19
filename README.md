# TAREA 1 Lenguajes de Programación (INF253) 2023-02
Programa en python que simula una calculadora especial mediante el uso de la librería **re**. Recibe un archivo llamado ***problemas.txt*** , el cual contiene operaciones que permiten la suma, resta, multiplicación y división(entera) de números enteros, además de las palabras clave *ANS* y *CUPON*. El programa retorna un archivo de texto llamado ***desarrollo.txt*** el cual contiene los resultados de las operaciones presentes en el archivo de problemas.

## CLAVES ANS Y CUPON
La palabra *ANS* funciona igual que en una calculadora normal. Al ser ingresada esta se reemplaza por el valor de la operación anterior.

La palabra *CUPON* recibe 1 o 2 parámetros (números enteros). Si recibe 1 retorna el 20% del número, si recibe 2 números (enteros), digamos, *x* e *y*, la función retornará el *y%* de *x*.

## ALGUNAS RESTRICCIONES
Los parentesis deben contener mínimo una operación dentro, esto es, si se ingresa, por ejemplo, `(1500)` esto será considerado error de sintáxis.
Las operaciones se ingresarán por bloques separados por un *whiteline* de la siguiente forma:
   ```
   2700 // 3 * 5 + 100
   86 + 14 * (CUPON(100)//2)
   (700 + 300) * ANS

   ANS * CUPON(23000, 50)
   2 +2
   ``` 
En caso de que haya error en una operación dentro de un bloque, ninguna se realizará. Se marcarán las sentencias que tengan error de sintáxis con la palabra *ERROR* y las que no tengan serán marcadas con *Sin Resolver*.
## EJECUCIÓN
Para la ejecución debe estar instalado python. Se puede ejecutar por consola mediante:
   ```
   python scriptname.py
   ```
Para el correcto funcionamiento el script debe estar en la misma carpeta que el archivo de texto *problemas.txt*.