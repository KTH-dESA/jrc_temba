python scripts/excel_to_osemosys.py input_data TEMBA_03_07_Ref.xlsx
python scripts/CBC_results_AS_MODEX.py output_data/output.txt

glpsol -m model/Temba_0406_modex.txt -d output_data/output.txt --wlp output_data/temba.lp --check

# Solve with CPLEX
rm -f mycplexcommands
touch mycplexcommands

echo "read output_data/temba.lp" > mycplexcommands
echo "optimize"             >> mycplexcommands
echo "write"                >> mycplexcommands
echo "output_data/temba.sol"    >> mycplexcommands
echo "quit"                 >> mycplexcommands

# Executes the cplex script written above
# Should set the path to CPLEX
cplex < mycplexcommands

# Solve with CBC
cbc temba.lp solve -solu output_data/solutionfile.txt

python scripts/transform_31072013.py output_data/temba.sol output_data/temba_solution.txt
sort output_data/temba_solution.txt -o output_data/temba_sorted.txt

wget https://raw.githubusercontent.com/OSeMOSYS/OSeMOSYS_GNU_MathProg/cplex_to_cbc/scripts/convert_cplex_to_cbc.py -O scripts/convert_cplex_to_cbc.py

python scripts/convert_cplex_to_cbc.py output_data/temba_sorted.txt output_data/temba_sorted_cbc.txt
