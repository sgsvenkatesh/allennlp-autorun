""" 
A sample file to show how you can automate running multiple models with small changes to the config. 
"""

import json
import os
from sys import platform
from gen_results import save_results

# CHANGE_HERE filename for the base config file
filename = "simple_tagger_pos"
# CHANGE_HERE identifier for the type of iterations, leave as empty if not needed
key = "encoders"
# CHANGE_HERE if you want to include your own packages, just enter the name like `neural_crf`
package = ""

# ---------------------------
""" CHANGE_HERE - configure the list you want to train on """

encodings_list = []
encoders = [
    { "type": "gru" },
    { "type": "lstm" },
    { "type": "rnn" },
]
params = {
    "input_size": 100,
    "hidden_size": 100,
    "num_layers": 2,
    "dropout": 0.5,
    "bidirectional": False
}

for encoding in encoders:
    encodings_list.append({ **encoding, **params })
# ---------------------------

fn_separator = "_" + key + "_"

with open("./test/config/" + filename + ".json") as f:
    data = json.load(f)
    
    for this_item in encodings_list:
        # CHANGE_HERE - adding the item to encoders object.
        data["model"]["encoder"] = this_item

        with open("./test/config/" + filename + fn_separator + str(this_item["type"]) + ".json", 'w') as outfile:
            json.dump(data, outfile, indent=4)

for this_item in encodings_list:
    os.system("rm -rf ./test/model/" + filename + fn_separator + str(this_item["type"]))
    os.system('python3 -m allennlp.run train ./test/config/' + filename + fn_separator + str(this_item["type"]) + '.json -s ./test/models/' + filename + fn_separator + str(this_item["type"]) + ((" --include-package " + package) if package else ""))

save_results(encodings_list, filename, fn_separator)

if platform == "darwin":
    # choose your alert tone here
    os.system("afplay /System/Library/PrivateFrameworks/ScreenReader.framework/Versions/A/Resources/Sounds/AnimationFlyToDownloads.aiff")






