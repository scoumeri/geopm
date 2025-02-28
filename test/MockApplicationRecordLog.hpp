/*
 * Copyright (c) 2015 - 2022, Intel Corporation
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 *
 *     * Redistributions of source code must retain the above copyright
 *       notice, this list of conditions and the following disclaimer.
 *
 *     * Redistributions in binary form must reproduce the above copyright
 *       notice, this list of conditions and the following disclaimer in
 *       the documentation and/or other materials provided with the
 *       distribution.
 *
 *     * Neither the name of Intel Corporation nor the names of its
 *       contributors may be used to endorse or promote products derived
 *       from this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 * "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 * LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
 * A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
 * OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 * SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
 * LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 * DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
 * THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY LOG OF THE USE
 * OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */

#ifndef MOCKAPPLICATIONRECORDLOG_HPP_INCLUDE
#define MOCKAPPLICATIONRECORDLOG_HPP_INCLUDE

#include "gmock/gmock.h"

#include "ApplicationRecordLog.hpp"

class MockApplicationRecordLog : public geopm::ApplicationRecordLog
{
    public:
        MOCK_METHOD(void, set_process, (int process), (override));
        MOCK_METHOD(void, set_time_zero, (const geopm_time_s &time), (override));
        MOCK_METHOD(void, enter, (uint64_t hash, const geopm_time_s &time), (override));
        MOCK_METHOD(void, exit, (uint64_t hash, const geopm_time_s &time), (override));
        MOCK_METHOD(void, epoch, (const geopm_time_s &time), (override));
        MOCK_METHOD(void, dump,
                    (std::vector<geopm::record_s> & records,
                     std::vector<geopm::short_region_s> &short_regions),
                    (override));
};

#endif
