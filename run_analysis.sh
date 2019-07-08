python scripts/excel_to_osemosys.py input_data TEMBA_03_07_Ref.xlsx
python scripts/CBC_results_AS_MODEX.py output_data/output.txt

glpsol -m model/Temba_0406_modex.txt -d output_data/output.txt --wlp temba.lp --check