MODELRUNS = ["TEMBA_16_08_Refer", "TEMBA_16_08_Refer_2020RET"]

rule all:
    input: ["output_data/{model_run}.txt".format(model_run=model_run) for model_run in MODELRUNS]

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
