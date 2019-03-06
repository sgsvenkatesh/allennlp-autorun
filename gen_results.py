import json

def save_results(iter_list, filename, fn_separator):
    results = {}
    
    for this_item in iter_list:
        try:
            with open("./test/model/" + filename + fn_separator + str(this_item["type"]) + "/metrics.json") as f:
                data = json.load(f)

                # choose the validation accuracy you want to store in th results
                results[this_item["type"]] = data["best_validation_accuracy3"]
        except FileNotFoundError:
            results[this_item["type"]] = "FileNotFoundError"

    with open("./test/results/autogen_results", "a") as outfile:
        outfile.write("_" + filename + "_" + fn_separator)
        outfile.write("\n------------------------\n")
        json.dump(json.loads(json.dumps(results)), outfile, indent=4)
        outfile.write("\n------------------------\n")