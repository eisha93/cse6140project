
#echo "hill climbing"
#python run_tsp.py burma14.tsp 3600 hill_climbing 12
#echo "--"
#python run_tsp.py ulysses16.tsp 3600 hill_climbing 154
#echo "--"
#python run_tsp.py berlin52.tsp 3600 hill_climbing 83
#echo "--"
#python run_tsp.py kroA100.tsp 3600 hill_climbing 44
#echo "--"
#python run_tsp.py ch150.tsp 3600 hill_climbing 3333
#echo "--"
#python run_tsp.py gr202.tsp 3600 hill_climbing 12345
#echo "--"
#echo "--"

echo "branch and bound"

#python run_tsp.py burma14.tsp 3600 branch_and_bound 12
#echo "--"
#python run_tsp.py ulysses16.tsp 3600 branch_and_bound 154
#echo "--"
python run_tsp.py berlin52.tsp 18000 branch_and_bound 83
echo "--"
python run_tsp.py kroA100.tsp 18000 branch_and_bound 44
echo "--"
python run_tsp.py ch150.tsp 18000 branch_and_bound 3333
echo "--"
python run_tsp.py gr202.tsp 18000 branch_and_bound 12345
echo "--"

