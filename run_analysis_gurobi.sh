#!/bin/bash
if [ "$1" != "" ]; then
    echo "Running model workflow for $1"
    MODEL_RUN_NAME=$1
    DATA_FOLDER=output_data

    INPUT_FILE=$MODEL_RUN_NAME.xlsx

    # This should be replaced by a model file downloaded from the OSeMOSYS repository (or a branch of the repository)
    MODEL_FILE=model/Temba_0406_modex.txt

    DATA_FILE=$DATA_FOLDER/$MODEL_RUN_NAME.txt
    LP_FILE=$DATA_FOLDER/$MODEL_RUN_NAME.lp.gz
    GUROBI_FILE=$DATA_FOLDER/$MODEL_RUN_NAME

    python scripts/excel_to_osemosys.py input_data $INPUT_FILE $DATA_FILE
    python scripts/CBC_results_AS_MODEX.py $DATA_FILE

    glpsol -m $MODEL_FILE -d $DATA_FILE --wlp $LP_FILE --check

    # Solve with Gurobi
    gurobi_cl NumericFocus=1 ResultFile=$GUROBI_FILE.sol ResultFile=$GUROBI_FILE.ilp LogFile=$GUROBI_FILE.log $LP_FILE
    sed '/ * 0$/d' $GUROBI_FILE.sol > results/$MODEL_RUN_NAME.sol # Remove zero value items

    # Create a folder in which to place the csv files computed by the generate_pickle script
    mkdir -p results/$MODEL_RUN_NAME

    # Generate the processed results files including csv files of computed results and a pickle file for the viewer
    python scripts/generate_pickle.py  output_data/$MODEL_RUN_NAME.txt results/$MODEL_RUN_NAME.sol gurobi results/$MODEL_RUN_NAME.pickle results/$MODEL_RUN_NAME

    python scripts/generate_results.py results/$MODEL_RUN_NAME.pickle $MODEL_RUN_NAME results/export_$MODEL_RUN_NAME

else
    echo "usage: bash $0 <model run name>"
    exit 1
fi
