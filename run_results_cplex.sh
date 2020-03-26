MODEL_RUN_NAME=TEMBA_Refer
DATA_FOLDER=output_data

MODEL_FILE=model/Temba_0406_modex.txt

DATA_FILE=$DATA_FOLDER/$MODEL_RUN_NAME.txt

python scripts/transform_31072013.py $DATA_FOLDER/$MODEL_RUN_NAME.sol $DATA_FOLDER/trans_$MODEL_RUN_NAME.txt
sort $DATA_FOLDER/trans_$MODEL_RUN_NAME.txt > $DATA_FOLDER/sorted_$MODEL_RUN_NAME.txt

curl https://raw.githubusercontent.com/OSeMOSYS/OSeMOSYS_GNU_MathProg/master/scripts/convert_cplex_to_cbc.py -o scripts/convert_cplex_to_cbc.py

python scripts/convert_cplex_to_cbc.py $DATA_FOLDER/sorted_$MODEL_RUN_NAME.txt results/$MODEL_RUN_NAME.cbc

mkdir results/$MODEL_RUN_NAME

python scripts/generate_pickle.py $DATA_FOLDER/$MODEL_RUN_NAME.txt results/$MODEL_RUN_NAME.cbc cbc results/$MODEL_RUN_NAME.pickle results/$MODEL_RUN_NAME

python scripts/generate_results.py results/$MODEL_RUN_NAME.pickle $MODEL_RUN_NAME results/export_$MODEL_RUN_NAME
