import csv
import os

def getCityBasedOnNr(cityList,nr):
    if (nr <= 0 or nr > len(cityList)):
        print("Something is wrong!")
        return cityList[0]
    else:
        return cityList[nr-1]    
    
def save_results_to_csv(results, filename):
    key = results[0].keys()
    output_path = os.path.join("output", filename)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, key)
        dict_writer.writeheader()
        dict_writer.writerows(results)