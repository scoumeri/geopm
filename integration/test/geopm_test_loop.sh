#!/bin/bash
#  Copyright (c) 2015 - 2022, Intel Corporation
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions
#  are met:
#
#      * Redistributions of source code must retain the above copyright
#        notice, this list of conditions and the following disclaimer.
#
#      * Redistributions in binary form must reproduce the above copyright
#        notice, this list of conditions and the following disclaimer in
#        the documentation and/or other materials provided with the
#        distribution.
#
#      * Neither the name of Intel Corporation nor the names of its
#        contributors may be used to endorse or promote products derived
#        from this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#  A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#  OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#  LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#  DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#  THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY LOG OF THE USE
#  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

COUNT=0
ERR=0
LOG_FILE=test_loop_output.log

while [ ${ERR} -eq 0 -a ${COUNT} -lt 10 ];
do
    COUNT=$((COUNT+1))
    echo "TEST LOOPER: Beginning loop ${COUNT}..." > >(tee -a ${LOG_FILE})
    python3 -m unittest discover \
            --top-level-directory ${GEOPM_SOURCE} \
            --start-directory ${GEOPM_SOURCE}/integration/test \
            --pattern 'test_*.py' \
            --verbose &> >(tee -a ${LOG_FILE})
    ERR=$?

    if [ ${ERR} -eq 0 ]; then
        # Requirements for service testing
        srun -N${SLURM_NNODES} -- sudo /usr/sbin/install_service.sh $(cat ${GEOPM_SOURCE}/VERSION) ${USER}
        python3 -m unittest discover \
                --top-level-directory ${GEOPM_SOURCE} \
                --start-directory ${GEOPM_SOURCE}/service/integration/test \
                --pattern 'test_*.py' \
                --verbose &> >(tee -a service_${LOG_FILE})
        ERR=$?
        srun -N${SLURM_NNODES} -- sudo /usr/sbin/install_service.sh --remove
    fi
done

#Do email only if there was a failure
if [ ${ERR} -ne 0 ]; then
    touch .tests_failed
fi

echo "Test looper done."

