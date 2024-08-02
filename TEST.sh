#!/usr/bin/bash

source <(curl https://raw.githubusercontent.com/torokmark/assert.sh/main/assert.sh --silent)
python scripts/antenna.measurement.nearFieldSamplingLength.py 1E9 --human
python scripts/propagation/lineOfSightDistance.py 0.5 # 2.524371
echo -e "1\\n4" | python scripts/propagation/lineOfSightDistance.py 4
3.57
7.14
python scripts/propagation/radioHorizon.py 0.5
2.913280
echo -e "1\\n4" | python scripts/propagation/radioHorizon.py 4
4.120000
8.240000
python scripts/propagation/pathLoss.py 1 10 --raw
52.45
echo -e "1 1\\n2E3 0.2" | python scripts/propagation/pathLoss.py --raw
32.45
84.4912
python scripts/measurement/planarScanLength.py 0.16 60 0.1 --raw
0.327128
echo -e "0.5 60 0.25\\n0.16 70 0.1" | python scripts/measurement/planarScanLength.py --raw
0.991025
0.489596
python scripts/measurement/planarScanViewAngle.py 0.327 0.16 0.1 --raw
59.9885
echo -e "0.991025 0.5 0.25\\n0.489596 0.16 0.1" | python scripts/measurement/planarScanViewAngle.py --raw
60
70