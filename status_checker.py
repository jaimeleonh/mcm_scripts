import json
import sys
sys.path.append('/afs/cern.ch/cms/PPD/PdmV/tools/McM/')
from rest import McM
from pprint import pprint

# Create McM instance, use default cookie location
mcm = McM(dev=False, id=McM.OIDC)

#tags="20240701_djarosla_SuuToSlSlToBSBS_preLegacy_FixedColors_161718"
#tags="20240901_bsirasva_LQLQToCMuCMu_Run2"
tags="20240604_dgadkari_RPVStopStopToJets_UDD323_161718"
#tags="20240727_huwang_RSGravitonWide"
#tags="20240902_bsirasva_LQLQToCMuCMu_run3"

requests = mcm.get('requests', query="tags={0}".format(tags))
# prepids = [request["prepid"] for request in req]

# for prepid in prepids:
    # mcm.approve('requests', prepid, None)

status = {}
results = {
    "Validation - Success": [],
    "Validation - Failed": [],
    "Validation - Ongoing": [],
    "Unknown": [],
    "Running": [],
    "Defined": [],
    "Done": [],
}

for req in requests:
    #pprint(req["history"][-1])
    #sys.exit()
    is_unknown = False
    status[req["prepid"]] = (req["history"][-1]["action"], req["history"][-1]["step"])
    if req["history"][-1]["action"] == "validation":
        if req["history"][-1]["step"] == "succeeded":
            results["Validation - Success"].append(req["prepid"])
        elif req["history"][-1]["step"] == "failed":
            results["Validation - Failed"].append(req["prepid"])
            # print(req["prepid"])
        else:
            is_unknown = True
    elif req["history"][-1]["action"] == "approve": # fix
        results["Validation - Ongoing"].append(req["prepid"])
    elif req["history"][-1]["action"] == "set status":
        if req["history"][-1]["step"] == "done":
            results["Done"].append(req["prepid"])
        elif req["history"][-1]["step"] == "defined":
            results["Defined"].append(req["prepid"])
        else:
            is_unknown = True
    elif req["history"][-1]["action"] == "wm priority":
            results["Running"].append(req["prepid"])
            #print(req["prepid"])
    else:
        is_unknown = True
    if is_unknown:
        #print(req["prepid"])
        #pprint(req["prepid"])
        # pprint(req["history"][-1])
        results["Unknown"].append(req["prepid"])

for key in results:
    print(key + ":", len(results[key]))
    # if key != "Done":
    #     for elem in results[key]:
    #         print(elem)

for prepid in results["Validation - Failed"]:
    print(f'"{prepid}",')
