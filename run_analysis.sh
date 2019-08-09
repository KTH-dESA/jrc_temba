MODEL_RUN_NAME=TEMBA_03_07_Ref
DATA_FOLDER=output_data

INPUT_FILE=$MODEL_RUN_NAME.xlsx

MODEL_FILE=model/Temba_0406_modex.txt

DATA_FILE=$DATA_FOLDER/$MODEL_RUN_NAME.txt

python scripts/excel_to_osemosys.py input_data $INPUT_FILE $DATA_FILE
python scripts/CBC_results_AS_MODEX.py $INPUT_FILE

glpsol -m $MODEL_FILE -d $DATA_FOLDER/output.txt --wlp $DATA_FOLDER/temba.lp --check

# Solve with CPLEX
rm -f mycplexcommands
touch mycplexcommands

echo "read $DATA_FOLDER/temba.lp" > mycplexcommands
echo "optimize" >> mycplexcommands
echo "write" >> mycplexcommands
echo "$DATA_FOLDER/temba.sol" >> mycplexcommands
echo "quit" >> mycplexcommands
cplex < mycplexcommands

python scripts/transform_31072013.py $DATA_FOLDER/temba.sol $DATA_FOLDER/temba_solution.txt
sort $DATA_FOLDER/temba_solution.txt -o $DATA_FOLDER/temba_sorted.txt

wget https://raw.githubusercontent.com/OSeMOSYS/OSeMOSYS_GNU_MathProg/cplex_to_cbc/scripts/convert_cplex_to_cbc.py -O scripts/convert_cplex_to_cbc.py

python scripts/convert_cplex_to_cbc.py $DATA_FOLDER/temba_sorted.txt $DATA_FOLDER/temba_sorted_cbc.txt

# Solve with CBC
cbc $DATA_FOLDER/temba.lp -dualpivot pesteep -psi 1.0 -pertv 52 -duals solve -solu $DATA_FOLDER/temba_sorted_cbc.txt

# Solve with Gurobi
gurobi_cl NumericFocus=1 ResultFile=$DATA_FOLDER/temba_gur.sol LogFile=$DATA_FOLDER/temba_gur.log $DATA_FOLDER/temba.lp
sed '/ * 0/d' $DATA_FOLDER/temba_gur.sol >> $DATA_FOLDER/temba_gur_nz.sol # Remove zero value items