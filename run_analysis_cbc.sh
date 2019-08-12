MODEL_RUN_NAME=TEMBA_03_07_Ref
DATA_FOLDER=output_data

INPUT_FILE=$MODEL_RUN_NAME.xlsx

MODEL_FILE=model/Temba_0406_modex.txt

DATA_FILE=$DATA_FOLDER/$MODEL_RUN_NAME.txt

python scripts/excel_to_osemosys.py input_data $INPUT_FILE $DATA_FILE
python scripts/CBC_results_AS_MODEX.py $INPUT_FILE

glpsol -m $MODEL_FILE -d $DATA_FOLDER/output.txt --wlp $DATA_FOLDER/$MODEL_RUN_NAME.lp.gz --check

# Solve with CBC
cbc $DATA_FOLDER/$MODEL_RUN_NAME.lp.gz -dualpivot pesteep -psi 1.0 -pertv 52 -duals solve -solu results/$MODEL_RUN_NAME.sol
