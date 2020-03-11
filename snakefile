MODELRUNS = ["TEMBA_Refer", "TEMBA_2oC", "TEMBA_1.5C"]

rule all:
    # input: ["results/{model_run}.pickle".format(model_run=model_run) for model_run in MODELRUNS]
    input: ["results/export_{model_run}".format(model_run=model_run) for model_run in MODELRUNS]

rule generate_model_file:
    input: 
        "input_data/{model_run}.xlsx"
    output: 
        "output_data/{model_run}.txt"
    threads: 
        2
    shell:
        "python scripts/excel_to_osemosys.py {input} {output}"

rule modify_model_file:
    input:  
        "output_data/{model_run}.txt"
    output: 
        "output_data/{model_run}_modex.txt"
    threads: 
        2
    shell:
        "python scripts/CBC_results_AS_MODEX.py {input} && cat {input} > {output}"

rule generate_lp_file:
    input: 
        "output_data/{model_run}_modex.txt"
    output: 
        protected("output_data/{model_run}.lp.gz")
    log: 
        "output_data/glpsol_{model_run}.log"
    threads: 
        1
    shell:
        "glpsol -m model/Temba_0406_modex.txt -d {input} --wlp {output} --check --log {log}"

rule solve_lp:
    input: 
        "output_data/{model_run}.lp.gz"
    output: 
        protected("output_data/{model_run}.sol")
    log: 
        "output_data/gurobi_{model_run}.log"
    threads: 
        2
    shell:
        "gurobi_cl NumericFocus=1 Method=2 Threads={threads} ResultFile={output} ResultFile=output_data/infeasible.ilp LogFile={log} {input}"

rule remove_zero_values:
    input: "output_data/{model_run}.sol"
    output: "results/{model_run}.sol"
    shell:
        "sed '/ * 0$/d' {input} > {output}"

rule generate_pickle:
    input: 
        results="results/{model_run}.sol", modelfile="output_data/{model_run}_modex.txt"
    output: 
        pickle="results/{model_run}.pickle", folder=directory("results/{model_run}")
    shell:
        "mkdir {output.folder} && python scripts/generate_pickle.py {input.modelfile} {input.results} gurobi {output.pickle} {output.folder}"

rule generate_results:
    input: 
        pickle="results/{model_run}.pickle"
    params:
        scenario="{model_run}"
    output: 
        folder=directory("results/export_{model_run}")
    conda:
        "envs/results.yaml"
    shell:
        "python scripts/generate_results.py {input.pickle} {params.scenario} {output.folder}"
