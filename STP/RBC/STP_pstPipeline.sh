
#!/bin/bash

# argv1: User

./STP_pstFraction.sh $1 PAN
./STP_pstProcess.sh $1 PAN
./STP_pstTraces.sh $1 PAN