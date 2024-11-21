import os
import argparse
import pickle
import glob
import numpy as np

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--tmp-dir', required=True)
    parser.add_argument('--overwrite', action='store_const', const=True,
                        default=False)
    args = vars(parser.parse_args())

    load(input_dir=args["tmp_dir"], overwrite=args["overwrite"])


def load(input_dir, overwrite):

    if input_dir[-1] != "/":
        input_dir += "/"

    files = glob.glob(input_dir+"*.p")

    if os.path.exists("results_ensemble.p") and not overwrite:
        results = np.load("results_ensemble.p")
        print("Loading results from disk")
    else:
        results = {"succesful_files": []}
        print("Creating new results file")

    files = [f for f in files if f not in results["succesful_files"]]
    print(len(files))
    for i, datafile in enumerate(files):

        print(i, datafile, end="\r")

        updaterate = float(datafile.split("_")[6])

        if updaterate not in results.keys():
            results[updaterate] = {"terr": [], "atmo": [], "foss": [], "ocea": [],
                                   "gmt": [], "econ": []}

        data = np.load(datafile)

        world = list(data["World.surface_air_temperature"].keys())[0]

        results[updaterate]["terr"].append(data["World.terrestrial_carbon"][world][-1])
        results[updaterate]["atmo"].append(data["World.atmospheric_carbon"][world][-1])
        results[updaterate]["foss"].append(data["World.fossil_carbon"][world][-1])
        results[updaterate]["ocea"].append(data["World.upper_ocean_carbon"][world][-1])
        results[updaterate]["gmt"].append(data["World.surface_air_temperature"][world][-1])

        social_systems = list(data["SocialSystem.has_emissions_tax"].keys())
        econ = [data["SocialSystem.economic_output_flow"][s][-1] for s in social_systems]
        results[updaterate]["econ"].append(econ)

        results["succesful_files"].append(datafile)

        pickle.dump(results, open("results_ensemble.p", "wb"))
