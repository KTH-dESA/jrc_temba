python scripts/excel_to_osemosys.py input_data TEMBA_03_07_Ref.xlsx
python scripts/CBC_results_AS_MODEX.py output_data/output.txt

glpsol -m model/Temba_0406_modex.txt -d output_data/output.txt --wlp output_data/temba.lp --check

# Solve with CPLEX
rm -f mycplexcommands
touch mycplexcommands

echo "read output_data/temba.lp" > mycplexcommands
echo "optimize" >> mycplexcommands
echo "write" >> mycplexcommands
echo "output_data/temba.sol" >> mycplexcommands
echo "quit" >> mycplexcommands
cplex < mycplexcommands

python scripts/transform_31072013.py output_data/temba.sol output_data/temba_solution.txt
sort output_data/temba_solution.txt -o output_data/temba_sorted.txt

wget https://raw.githubusercontent.com/OSeMOSYS/OSeMOSYS_GNU_MathProg/cplex_to_cbc/scripts/convert_cplex_to_cbc.py -O scripts/convert_cplex_to_cbc.py

python scripts/convert_cplex_to_cbc.py output_data/temba_sorted.txt output_data/temba_sorted_cbc.txt

# Solve with CBC
cbc output_data/temba.lp solve -solu output_data/temba_sorted_cbc.txt

# Solve with Gurobi
gurobi_cl NumericFocus=1 ResultFile=output_data/temba_gur.sol LogFile=output_data/temba_gur.log output_data/temba.lp
sed '/ * 0/d' output_data/temba_gur.sol >> output_data/temba_gur_nz.sol # Remove zero value items