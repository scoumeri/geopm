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

#ifndef EPOCHIOGROUP_HPP_INCLUDE
#define EPOCHIOGROUP_HPP_INCLUDE

#include <memory>

#include "geopm/IOGroup.hpp"

namespace geopm
{
    class PlatformTopo;
    class ApplicationSampler;

    class EpochIOGroup : public IOGroup
    {
        public:
            EpochIOGroup();
            EpochIOGroup(const PlatformTopo &topo,
                         ApplicationSampler &app);
            virtual ~EpochIOGroup() = default;
            std::set<std::string> signal_names(void) const override;
            std::set<std::string> control_names(void) const override;
            bool is_valid_signal(const std::string &signal_name) const override;
            bool is_valid_control(const std::string &control_name) const override;
            int signal_domain_type(const std::string &signal_name) const override;
            int control_domain_type(const std::string &control_name) const override;
            int push_signal(const std::string &signal_name, int domain_type, int domain_idx)  override;
            int push_control(const std::string &control_name, int domain_type, int domain_idx) override;
            void read_batch(void) override;
            void write_batch(void) override;
            double sample(int batch_idx) override;
            void adjust(int batch_idx, double setting) override;
            double read_signal(const std::string &signal_name, int domain_type, int domain_idx) override;
            void write_control(const std::string &control_name, int domain_type, int domain_idx, double setting) override;
            void save_control(void) override;
            void restore_control(void) override;
            std::function<double(const std::vector<double> &)> agg_function(const std::string &signal_name) const override;
            std::function<std::string(double)> format_function(const std::string &signal_name) const override;
            std::string signal_description(const std::string &signal_name) const override;
            std::string control_description(const std::string &control_name) const override;
            int signal_behavior(const std::string &signal_name) const override;
            void save_control(const std::string &save_path) override;
            void restore_control(const std::string &save_path) override;
            std::string name(void) const override;
            static std::string plugin_name(void);
            static std::unique_ptr<IOGroup> make_plugin(void);
        private:
            static const std::set<std::string> m_valid_signal_name;
            void init(void);
            void check_domain(int domain_type, int domain_idx) const;
            void check_signal_name(const std::string &signal_name) const;

            const PlatformTopo &m_topo;
            const ApplicationSampler &m_app;
            int m_num_cpu;
            std::vector<double> m_per_cpu_count;
            std::map<int, std::set<int> > m_process_cpu_map;
            bool m_is_batch_read;
            bool m_is_initialized;
            std::map<int, int> m_cpu_signal_map;
            std::vector<int> m_active_signal;
    };
}

#endif
