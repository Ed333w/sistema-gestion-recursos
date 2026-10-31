#!/bin/bash
# Uso: repro.sh <carpeta_proyecto> <carpeta_salida>
# Ejecuta los 7 comandos de la sección 3 del prompt y guarda cada salida.
cd "$1" || exit 1
OUT="$2"; mkdir -p "$OUT"
export PYTHONIOENCODING=utf-8
run() { printf "$2" | python main.py > "$OUT/$1.txt" 2>&1; echo "exit=$?" >> "$OUT/$1.txt"; }
run E1  '4\n1\nU001\nR0001\nCentro\n\n3\n\n0\n0\n'
run E2  '1\n1\n\n\n\n0\n0\n'
run E3E4 '4\n1\nU001\nR0001\nCentro\n\n1\nU002\nR0001\nCentro\n\n0\n3\n\n0\n'
run E5  '4\n2\nP9999\n\n0\n0\n'
run E6  '5\n1\nR0001\n\n2\nR0001\n\n0\n0\n'
run E7  '6\n1\nC1\nIngenieria\n\n1\nC1\nRepetida\n\n2\nC1\n\n0\n0\n'
run E8  '4\n1\nU001\nR0001\nCentro\n\n0\n7\n1\n\n2\n\n0\n0\n'
