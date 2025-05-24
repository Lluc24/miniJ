#! /bin/bash

python_script="g.py"
path_tests="tests"

for test_file in $path_tests/*.j
do
  test_name=$(basename "$test_file" .j)
	expected_output="${path_tests}/${test_name}.out"
	actual_output="${path_tests}/${test_name}.tmp"
	python $python_script $test_file > $actual_output
	echo "Differences between $expected_output and $actual_output:"
	echo "------------------------------------------------------------------"
	echo "------------------------------------------------------------------"
	diff $expected_output $actual_output
	echo "------------------------------------------------------------------"
	echo "------------------------------------------------------------------"
	rm $actual_output
done