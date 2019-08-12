MODEL_RUN_NAME=TEMBA_03_07_Ref
DATA_FOLDER=output_data

INPUT_FILE=$MODEL_RUN_NAME.xlsx

MODEL_FILE=model/Temba_0406_modex.txt

DATA_FILE=$DATA_FOLDER/$MODEL_RUN_NAME.txt

python scripts/excel_to_osemosys.py input_data $INPUT_FILE $DATA_FILE
python scripts/CBC_results_AS_MODEX.py $INPUT_FILE

glpsol -m $MODEL_FILE -d $DATA_FOLDER/$DATA_FILE --wlp $DATA_FOLDER/$MODEL_RUN_NAME.lp.gz --check

# Solve with CPLEX
rm -f mycplexcommands
touch mycplexcommands

echo "read $DATA_FOLDER/$MODEL_RUN_NAME.lp.gz" > mycplexcommands
echo "optimize" >> mycplexcommands
echo "write" >> mycplexcommands
echo "$DATA_FOLDER/$MODEL_RUN_NAME.sol" >> mycplexcommands
echo "quit" >> mycplexcommands
cplex < mycplexcommands

python scripts/transform_31072013.py $DATA_FOLDER/$MODEL_RUN_NAME.sol $DATA_FOLDER/$MODEL_RUN_NAME.txt
sort $DATA_FOLDER/$MODEL_RUN_NAME.txt > $DATA_FOLDER/sorted_$MODEL_RUN_NAME.txt

curl https://raw.githubusercontent.com/OSeMOSYS/OSeMOSYS_GNU_MathProg/master/scripts/convert_cplex_to_cbc.py -o scripts/convert_cplex_to_cbc.py

python scripts/convert_cplex_to_cbc.py $DATA_FOLDER/sorted_$MODEL_RUN_NAME.txt results/$MODEL_RUN_NAME.sol

python scripts/generate_pickle.py results/$MODEL_RUN_NAME.sol results/$MODEL_RUN_NAME.pickle