import csv, os, pandas

def manipulate_csv(input_file, output_file):
    with open(input_file) as f:
          data = pandas.read_csv(input_file)
          data['Temperature']+=5
          data.to_csv(output_file)

def main():
    input_file = "../data/input.csv"
    output_file = "output.csv"
    manipulate_csv(input_file, output_file)

if __name__ == "__main__":
    main()
