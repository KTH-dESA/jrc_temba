MODELRUNS = ["TEMBA_23_08_1.5C_2020RET", "TEMBA_27_08_1.5C_2020RET_EV"]

rule all:
    input: ["results/{model_run}.pickle".format(model_run=model_run) for model_run in MODELRUNS]

rule generate_model_file:
    input: "input_data/{model_run}.xlsx"
    output: "output_data/{model_run}.txt"
    shell:
        "python scripts/excel_to_osemosys.py {input} {output}"

rule modify_model_file:
    input: rules.generate_model_file.output
    output: "output_data/{model_run}_modex.txt"
    shell:
        "python scripts/CBC_results_AS_MODEX.py {input}"

rule generate_lp_file:
    input: "output_data/{model_run}_modex.txt"
    output: "output_data/{model_run}.lp.gz"
    shell:
        "glpsol -m model/Temba_0406_modex.txt -d {input} --wlp {output} --check"

rule solve_lp:
    input: "output_data/{model_run}.lp.gz"
    output: solution="output_data/{model_run}.sol",infeasible="output_data/{model_run}.ilp",logfile="output_data/{model_run}.log"
    shell:
        "gurobi_cl NumericFocus=1 Method=2 Threads={threads} ResultFile={output.solution} ResultFile={output.infeasible} LogFile={output.logfile} {input}"

rule remove_zero_values:
    input: "output_data/{model_run}.sol"
    output: "results/{model_run}.sol"
    shell:
        "sed '/ * 0$/d' {input} > {output}"

rule generate_pickle:
    input: "results/{model_run}.sol"
    output: pickle="results/{model_run}.pickle", modelfile="output_data/{model_run}_modex.txt", folder=directory("results/{model_run}")
    shell:
        "python scripts/generate_pickle.py {output.modelfile}  {input} gurobi {output.pickle} {output.folder}"