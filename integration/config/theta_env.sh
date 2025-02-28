#!/bin/bash
#
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

# THETA BUILD ENVIRONMENT
#
# This script is intended to be sourced within an existing script or shell ONLY.
# It is NOT intended to be ./ executed.

module unload darshan

export CC='cc -dynamic'
export CXX='CC -dynamic'
export MPICC='cc -dynamic'
export MPICXX='CC -dynamic'
export FC=ftn
export F77=ftn
export F90=ftn
export MPIFORT=ftn
export MPIFC=ftn
export MPIF77=ftn
export MPIF90=ftn

AVX_FLAG='-xCORE-AVX2'
export CFLAGS=${AVX_FLAG}
export CXXFLAGS=${AVX_FLAG}
export FCFLAGS="-dynamic ${AVX_FLAG}"
export FFLAGS="-dynamic ${AVX_FLAG}"

