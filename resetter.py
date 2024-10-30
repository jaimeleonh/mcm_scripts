import json
import sys
sys.path.append('/afs/cern.ch/cms/PPD/PdmV/tools/McM/')
from rest import McM
import time

# Create McM instance, use default cookie location
mcm = McM(dev=False, id=McM.OIDC)

tags="20240930_shjeon_ZptoLL"

req = mcm.get('requests', query="tags={0}".format(tags))
prepids = [request["prepid"] for request in req]

for prepid in prepids:
    print(prepid)
    mcm.approve('requests', prepid, 0)
    time.sleep(1)
