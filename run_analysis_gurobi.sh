MODEL_RUN_NAME=TEMBA_09_08_Ref
DATA_FOLDER=output_data

INPUT_FILE=$MODEL_RUN_NAME.xlsx

MODEL_FILE=model/Temba_0406_modex.txt

DATA_FILE=$DATA_FOLDER/$MODEL_RUN_NAME.txt
LP_FILE=$DATA_FOLDER/$MODEL_RUN_NAME.lp.gz
GUROBI_FILE=$DATA_FOLDER/$MODEL_RUN_NAME

python scripts/excel_to_osemosys.py input_data $INPUT_FILE $DATA_FILE
python scripts/CBC_results_AS_MODEX.py $DATA_FILE

glpsol -m $MODEL_FILE -d $DATA_FILE --wlp $LP_FILE --check

# Solve with Gurobi
gurobi_cl NumericFocus=1 ResultFile=$GUROBI_FILE.sol LogFile=$GUROBI_FILE.log $LP_FILE
sed '/ * 0/d' $GUROBI_FILE.sol >> results/$GUROBI_FILE.sol # Remove zero value items
