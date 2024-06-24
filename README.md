## Requirements
Installing [PySAT](https://pysathq.github.io/):
```
pip install python-sat[aiger,approxmc,cryptosat,pblib]
```
(see PySAT's [dependencies](https://pysathq.github.io/installation/)).

## Usage
```
git clone https://github.com/yotamfe/grid-dislocation-py-sat-solver
cd grid-dislocation-py-sat-solver
```
The code can be used in the following ways:
### Solving random realizations
For C2 grid dislocation problems:
```
python run_c2.py -l <lattice size> -n <num random realizations> -p <dislocation probability>
```
And likewise for C6:
```
python run_c6.py -l <lattice size> -n <num random realizations> -p <dislocation probability>
```
For example, to solve 10 random realizations
of the 4x4x4 grid dislocation problem with 10 percent dislocation density,
```
python run_c2.py -l 4 -n 10 -p 0.1
```
The output should look (e.g.) like this:
```
Running 10 realizations of size 4x4x4 with 10.0% random dislocations
Running realization 0
Solution found
Running realization 1
Solution found
Running realization 2
Solution found
Running realization 3
Solution found
Running realization 4
Solution found
Running realization 5
Solution found
Running realization 6
Solution found
Running realization 7
Solution found
Running realization 8
Solution found
Running realization 9
Solution found...
```
The last realization is always stored in a file called `latest_lattice.txt` in the current directory. (We can change this to something more configurable of course :))

### Solving given realizations
Alternatively, you can use a method of your choice to generate a text file
describing a dislocation configuration, in the same format as the output file
generated by the program. Then, you can run the following utility to test it
for the existence of a solution. For C2,
```
python solve_from_file_c2.py -i <input_file>
```
And similarly for C6,
```
python solve_from_file_c6.py -i <input_file>
```


