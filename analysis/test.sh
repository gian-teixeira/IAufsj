DATA=data/input/*
OUTPUT=data/output
EXEC='python3 ../tsp.py'

DEFAULT_ITER=100
DEFAULT_PART=1
ITERS=$(seq 100 10 1000)
PARTS=$(seq 0.5 0.25 2 | sed 's/,/./g')

for input in $DATA; do
	file_name=$(basename $input)
	output_folder=$OUTPUT/${file_name%.*}
	mkdir -p $output_folder

	# Variando o numero de particulas
	for p in $PARTS; do
		read N < $input
		N=$(echo "$N * $p" | bc)
		N=${N%.*}

		output_file=$output_folder/particle_count_$N
		time=$({ $(which time) -f "%e" $EXEC 100 $N < $input > $output_file; } 2>&1)
		echo -e "$time\n$(cat $output_file)" > $output_file
	done

	continue

	# Variando numero de iteracoes
	for i in $ITERS; do 
		output_file=$output_folder/iterations_$i
		time=$({ $(which time) -f "%e" $EXEC $i $DEFAULT_PART < $input > $output_file; } 2>&1)
		echo -e "$time\n$(cat $output_file)" > $output_file
	done
done
