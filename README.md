# csv_set_diff
Computes the set difference `A \ B` of two CSV files `A.csv` and `B.csv`, using one column as the primary key (by default, the 0th column is used).
The `A \ B` result is printed to stdout in CSV format as a subset of `A`.

## Usage

```
$ python3 csv_set_diff.py -h
usage: csv_set_diff.py [-h] [--ignore-header-row] CSV1_PATH CSV2_PATH [PRIMARY_KEY_COLUMN_INDEX] [CONSTRAINTS ...]

Computes the set difference A \ B of two CSV files A.csv and B.csv.

positional arguments:
  CSV1_PATH             Path to the first CSV file (the A in A \ B).
  CSV2_PATH             Path to the second CSV file (the B in A \ B).
  PRIMARY_KEY_COLUMN_INDEX
                        Index of the primary key column (0-based). If not provided, the 0-th column is used.
  CONSTRAINTS           An optional list of constraints (enacted on both CSV input files). Supported operators: EQ, LT, GT. Example (value of 3rd column shall be greater than
                        zero): 3GT0

options:
  -h, --help            show this help message and exit
  --ignore-header-row   Ignore the 0th row of both CSV input files.

```

## Example

```
$ cat exampleA.csv 
Alice,Wonderland,12
Bob,Builder,34
Charlie,Chaplin,56
John,Doe,78
```

```
$ cat exampleB.csv 
Bob,Bauer,12
Charlie,Chaplin,34
```

```
$ python3 csv_set_diff.py exampleA.csv exampleB.csv
Alice,Wonderland,12
John,Doe,78
```

```
$ python3 csv_set_diff.py exampleA.csv exampleB.csv 1
Alice,Wonderland,12
Bob,Builder,34
John,Doe,78
```
