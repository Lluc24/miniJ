#! /bin/bash

script="g.py"
directori_tests="tests"

for fitxer_test in $directori_tests/*.j
do
  nom_test=$(basename "$fitxer_test" .j)
	sortida_esperada="${directori_tests}/${nom_test}.out"
	sortida_obtinguda="${directori_tests}/${nom_test}.tmp"
	python $script "$fitxer_test" > "$sortida_obtinguda"
	echo "Diferencies entre $sortida_esperada i $sortida_obtinguda:"
	diff "$sortida_esperada" "$sortida_obtinguda"
	rm "$sortida_obtinguda"
done