#!/usr/bin/env python3
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

import unittest
from unittest import mock
import os
import stat
import tempfile
from pathlib import Path

from geopmdpy.system_files import secure_make_dirs
from geopmdpy.system_files import secure_make_file
from geopmdpy.system_files import secure_read_file

class TestSecureFiles(unittest.TestCase):
    def setUp(self):
        """Create temporary directory

        """
        self._test_name = 'TestSecureFiles'
        self._TEMP_DIR = tempfile.TemporaryDirectory(self._test_name)

    def tearDown(self):
        """Clean up temporary directory

        """
        self._TEMP_DIR.cleanup()

    def check_dir_perms(self, path):
        """Assert that the path points to a file with mode 0o700
        Assert that the user and group have the right permissions.

        """
        st = os.stat(path)
        perm_mode = stat.S_IMODE(st.st_mode)
        user_owner = st.st_uid
        group_owner = st.st_gid
        self.assertEqual(0o700, perm_mode)
        self.assertEqual(os.getuid(), user_owner)
        self.assertEqual(os.getgid(), group_owner)

    def check_file_perms(self, path):
        """Assert that the path points to a file with mode 0o600
        Assert that the user and group have the right permissions.

        """
        st = os.stat(path)
        perm_mode = stat.S_IMODE(st.st_mode)
        user_owner = st.st_uid
        group_owner = st.st_gid
        self.assertEqual(0o600, perm_mode)
        self.assertEqual(os.getuid(), user_owner)
        self.assertEqual(os.getgid(), group_owner)

    def test_pre_exists(self):
        """Usage of pre existing geopm-service directory

        Test calls secure_make_dirs() when the geopm-service
        directory has already been created.

        """
        sess_path = f'{self._TEMP_DIR.name}/geopm-service'
        os.mkdir(sess_path, mode=0o700)
        secure_make_dirs(sess_path)
        self.check_dir_perms(sess_path)

    def test_default_creation(self):
        """Default creation of geopm-service directory

        Test calls secure_make_dirs() when the geopm-service
        directory is not present.

        """
        sess_path = f'{self._TEMP_DIR.name}/geopm-service'
        secure_make_dirs(sess_path)
        self.check_dir_perms(sess_path)

    def test_creation_link_not_dir(self):
        """The path specified is a link not a directory.

        Test calls secure_make_dirs() when the geopm-service
        provided path is not a directory, but a link. It asserts that
        a warning message is printed to standard error and that a
        new directory is created while the link is renamed.

        """
        sess_path = f'{self._TEMP_DIR.name}/geopm-service-link'
        os.symlink('/tmp', sess_path)
        with mock.patch('os.path.islink', wraps=os.path.islink) as mock_os_path_islink, \
             mock.patch('uuid.uuid4', return_value='uuid4'), \
             mock.patch('sys.stderr.write', return_value=None) as mock_sys_stderr_write:
            secure_make_dirs(sess_path)
            renamed_path = f'{sess_path}-uuid4-INVALID'
            calls = [
                mock.call(f'Warning: <geopm-service> {sess_path} is a symbolic link, the link will be renamed to {renamed_path}\n'),
                mock.call(f'Warning: <geopm-service> the symbolic link points to /tmp\n')
            ]
            mock_sys_stderr_write.assert_has_calls(calls)
            mock_os_path_islink.assert_called_once_with(sess_path)
        self.assertTrue(os.path.exists(renamed_path))
        self.check_dir_perms(sess_path)

    def test_creation_file_not_dir(self):
        """The path specified is a file not a directory.

        Test calls secure_make_dirs() when the geopm-service
        provided path is not a directory, but a file. It asserts that
        a warning message is printed to standard error and that a
        new directory is created while the file is renamed.

        """
        sess_path = f'{self._TEMP_DIR.name}/geopm-service.txt'
        filename = Path(sess_path)
        filename.touch(exist_ok=True)

        with mock.patch('os.path.islink', wraps=os.path.islink) as mock_os_path_islink, \
             mock.patch('os.path.isdir', wraps=os.path.isdir) as mock_os_path_isdir, \
             mock.patch('uuid.uuid4', return_value='uuid4'), \
             mock.patch('sys.stderr.write', return_value=None) as mock_sys_stderr_write:
            secure_make_dirs(sess_path)
            renamed_path = f'{sess_path}-uuid4-INVALID'
            msg = f'Warning: <geopm-service> {sess_path} is not a directory, it will be renamed to {renamed_path}\n'
            mock_sys_stderr_write.assert_called_once_with(msg)
            mock_os_path_islink.assert_called_once_with(sess_path)
            mock_os_path_isdir.assert_called_once_with(sess_path)
        self.assertTrue(os.path.exists(renamed_path))
        self.check_dir_perms(sess_path)

    def test_creation_bad_perms(self):
        """Directory exists with bad permissions

        Test calls secure_make_dirs() when the geopm-service
        directory is present with wrong permissions.  It asserts that
        a warning message is printed to standard error and that the
        permissions are changed.

        """
        sess_path = f'{self._TEMP_DIR.name}/geopm-service'
        os.mkdir(sess_path, mode=0o755)

        with mock.patch('os.stat', wraps=os.stat) as mock_os_stat, \
             mock.patch('os.path.islink', wraps=os.path.islink) as mock_os_path_islink, \
             mock.patch('os.path.isdir', wraps=os.path.isdir) as mock_os_path_isdir, \
             mock.patch('uuid.uuid4', return_value='uuid4'), \
             mock.patch('sys.stderr.write', return_value=None) as mock_sys_stderr_write:
            secure_make_dirs(sess_path)
            renamed_path = f'{sess_path}-uuid4-INVALID'
            calls = [
                mock.call(f'Warning: <geopm-service> {sess_path} has wrong permissions, it will be renamed to {renamed_path}\n'),
                mock.call(f'Warning: <geopm-service> the wrong permissions were 0o755\n')
            ]
            mock_sys_stderr_write.assert_has_calls(calls)
            # os.stat() is also called internally by system functions like maybe os.path.islink()
            mock_os_stat.assert_called_with(sess_path)
            mock_os_path_islink.assert_called_once_with(sess_path)
            mock_os_path_isdir.assert_called_once_with(sess_path)
        self.assertTrue(os.path.exists(renamed_path))
        self.check_dir_perms(sess_path)

    def test_creation_bad_user_owner(self):
        """Directory exists with wrong user owner

        Test calls secure_make_dirs() when the geopm-service
        directory is present with wrong ownership.  It asserts that
        a warning message is printed to standard error and that the
        ownership is changed.

        """
        sess_path = f'{self._TEMP_DIR.name}/geopm-service'
        os.mkdir(sess_path, mode=0o700)

        bad_user = mock.create_autospec(os.stat_result, spec_set=True)
        bad_user.st_uid = os.getuid() + 1
        bad_user.st_gid = os.getgid()
        bad_user.st_mode = 0o700

        with mock.patch('os.stat', return_value=bad_user) as mock_os_stat, \
             mock.patch('os.path.islink', return_value=False) as mock_os_path_islink, \
             mock.patch('os.path.isdir', return_value=True) as mock_os_path_isdir, \
             mock.patch('uuid.uuid4', return_value='uuid4'), \
             mock.patch('sys.stderr.write', return_value=None) as mock_sys_stderr_write:
            secure_make_dirs(sess_path)
            renamed_path = f'{sess_path}-uuid4-INVALID'
            calls = [
                mock.call(f'Warning: <geopm-service> {sess_path} has wrong user owner, it will be renamed to {renamed_path}\n'),
                mock.call(f'Warning: <geopm-service> the wrong user owner was {bad_user.st_uid}\n')
            ]
            mock_sys_stderr_write.assert_has_calls(calls)
            # os.stat() is also called internally by system functions like maybe os.path.islink()
            mock_os_stat.assert_called_with(sess_path)
            mock_os_path_islink.assert_called_once_with(sess_path)
            mock_os_path_isdir.assert_called_once_with(sess_path)
        self.assertTrue(os.path.exists(renamed_path))
        self.check_dir_perms(sess_path)

    def test_creation_bad_group_owner(self):
        """Directory exists with wrong group owner

        Test calls secure_make_dirs() when the geopm-service
        directory is present with wrong ownership.  It asserts that
        a warning message is printed to standard error and that the
        ownership is changed.

        """
        sess_path = f'{self._TEMP_DIR.name}/geopm-service'
        os.mkdir(sess_path, mode=0o700)

        bad_group = mock.create_autospec(os.stat_result, spec_set=True)
        bad_group.st_uid = os.getuid()
        bad_group.st_gid = os.getgid() + 1
        bad_group.st_mode = 0o700

        with mock.patch('os.stat', return_value=bad_group) as mock_os_stat, \
             mock.patch('os.path.islink', return_value=False) as mock_os_path_islink, \
             mock.patch('os.path.isdir', return_value=True) as mock_os_path_isdir, \
             mock.patch('uuid.uuid4', return_value='uuid4'), \
             mock.patch('sys.stderr.write', return_value=None) as mock_sys_stderr_write:
            secure_make_dirs(sess_path)
            renamed_path = f'{sess_path}-uuid4-INVALID'
            calls = [
                mock.call(f'Warning: <geopm-service> {sess_path} has wrong group owner, it will be renamed to {renamed_path}\n'),
                mock.call(f'Warning: <geopm-service> the wrong group owner was {bad_group.st_gid}\n')
            ]
            mock_sys_stderr_write.assert_has_calls(calls)
            # os.stat() is also called internally by system functions like maybe os.path.islink()
            mock_os_stat.assert_called_with(sess_path)
            mock_os_path_islink.assert_called_once_with(sess_path)
            mock_os_path_isdir.assert_called_once_with(sess_path)
        self.assertTrue(os.path.exists(renamed_path))
        self.check_dir_perms(sess_path)

    def test_read_file_not_exists(self):
        """File to be securely read in does not exist!

        Creates the geopm-service directory, but does not create the file within.
        Calls secure_read_file() with a non existent file path.

        """
        dir_path = f'{self._TEMP_DIR.name}/geopm-service'
        os.mkdir(dir_path, mode=0o700)
        self.check_dir_perms(dir_path)
        file_name = "stuff.json"
        full_file_path = os.path.join(dir_path, file_name)
        # do not create the file

        with mock.patch('sys.stderr.write', return_value=None) as mock_sys_stderr_write:
            contents = secure_read_file(full_file_path)
            self.assertIsNone(contents)
            mock_sys_stderr_write.assert_called_once_with(f'Warning: <geopm-service> {full_file_path} does not exist\n')
        self.assertFalse(os.path.exists(full_file_path))

    def test_read_file_is_directory(self):
        """File to be securely read in is actually a directory!

        Creates the geopm-service directory, and creates another directory within.
        Calls secure_read_file() with a directory instead of a file.

        """
        dir_path = f'{self._TEMP_DIR.name}/geopm-service'
        os.mkdir(dir_path, mode=0o700)
        self.check_dir_perms(dir_path)
        file_name = "stuff.json"
        full_file_path = os.path.join(dir_path, file_name)
        renamed_path = f'{full_file_path}-uuid4-INVALID'
        # create full_file_path as a directory instead of creating a file
        os.mkdir(full_file_path, mode=0o700)

        with mock.patch('uuid.uuid4', return_value='uuid4'), \
             mock.patch('sys.stderr.write', return_value=None) as mock_sys_stderr_write:
            contents = secure_read_file(full_file_path)
            self.assertIsNone(contents)
            mock_sys_stderr_write.assert_called_once_with(f'Warning: <geopm-service> {full_file_path} is a directory, it will be renamed to {renamed_path}\n')
        self.assertFalse(os.path.exists(full_file_path))
        self.assertTrue(os.path.exists(renamed_path))

    def test_read_file_is_link(self):
        """File to be securely read in is actually a link!

        Creates the geopm-service directory, and creates a link within.
        Calls secure_read_file() with a link instead of a file.

        """
        dir_path = f'{self._TEMP_DIR.name}/geopm-service'
        os.mkdir(dir_path, mode=0o700)
        self.check_dir_perms(dir_path)
        file_name = "stuff.json"
        full_file_path = os.path.join(dir_path, file_name)
        renamed_path = f'{full_file_path}-uuid4-INVALID'
        # create full_file_path as a link instead of creating a file
        os.symlink('/tmp', full_file_path)

        with mock.patch('os.path.exists', wraps=os.path.exists) as mock_os_path_exists, \
             mock.patch('os.path.islink', wraps=os.path.islink) as mock_os_path_islink, \
             mock.patch('os.readlink', wraps=os.readlink) as mock_os_readlink, \
             mock.patch('uuid.uuid4', return_value='uuid4'), \
             mock.patch('sys.stderr.write', return_value=None) as mock_sys_stderr_write:
            contents = secure_read_file(full_file_path)
            self.assertIsNone(contents)
            calls = [
                mock.call(f'Warning: <geopm-service> {full_file_path} is a symbolic link, it will be renamed to {renamed_path}\n'),
                mock.call(f'Warning: <geopm-service> the symbolic link points to /tmp\n')
            ]
            mock_sys_stderr_write.assert_has_calls(calls)
            mock_os_path_exists.assert_called_once_with(full_file_path)
            mock_os_path_islink.assert_called_once_with(full_file_path)
            mock_os_readlink.assert_called_once_with(full_file_path)

    def test_read_file_is_fifo(self):
        """File to be securely read in is actually a fifo!

        Creates the geopm-service directory, and creates a fifo within.
        Calls secure_read_file() with a fifo instead of a file.

        """
        dir_path = f'{self._TEMP_DIR.name}/geopm-service'
        os.mkdir(dir_path, mode=0o700)
        self.check_dir_perms(dir_path)
        file_name = "stuff.json"
        full_file_path = os.path.join(dir_path, file_name)
        renamed_path = f'{full_file_path}-uuid4-INVALID'
        # create full_file_path as a fifo instead of creating a regular file
        os.mkfifo(full_file_path)

        with mock.patch('os.path.exists', wraps=os.path.exists) as mock_os_path_exists, \
             mock.patch('os.path.islink', wraps=os.path.islink) as mock_os_path_islink, \
             mock.patch('os.stat', wraps=os.stat) as mock_os_stat, \
             mock.patch('uuid.uuid4', return_value='uuid4'), \
             mock.patch('sys.stderr.write', return_value=None) as mock_sys_stderr_write:
            contents = secure_read_file(full_file_path)
            self.assertIsNone(contents)
            mock_sys_stderr_write.assert_called_once_with(f'Warning: <geopm-service> {full_file_path} is not a regular file, it will be renamed to {renamed_path}\n')
            mock_os_path_exists.assert_called_once_with(full_file_path)
            mock_os_path_islink.assert_called_once_with(full_file_path)
            # os.stat() is also called internally by system functions like maybe os.path.islink()
            # also we are calling it explicitly in order to determine if the file is a fifo,
            # to keep the application from trying to open it, and blocking the process.
            mock_os_stat.assert_called()
        self.assertFalse(os.path.exists(full_file_path))
        self.assertTrue(os.path.exists(renamed_path))

    def test_read_file_bad_permissions(self):
        """File to be securely read in has wrong permissions.

        Creates the geopm-service directory, and creates a regular file with wrong permissions within.
        Calls secure_read_file() with that file.

        """
        dir_path = f'{self._TEMP_DIR.name}/geopm-service'
        os.mkdir(dir_path, mode=0o700)
        self.check_dir_perms(dir_path)
        file_name = "stuff.json"
        full_file_path = os.path.join(dir_path, file_name)
        renamed_path = f'{full_file_path}-uuid4-INVALID'
        # Create the full_file_path but with the wrong permissions.
        filename = Path(full_file_path)
        filename.touch(mode=0o644, exist_ok=True)
        expected_mode = 0o644 | stat.S_IFREG

        with mock.patch('os.path.exists', wraps=os.path.exists) as mock_os_path_exists, \
             mock.patch('os.path.isdir', wraps=os.path.isdir) as mock_os_path_isdir, \
             mock.patch('os.path.islink', wraps=os.path.islink) as mock_os_path_islink, \
             mock.patch('os.stat', wraps=os.stat) as mock_os_stat, \
             mock.patch('stat.S_ISREG', wraps=stat.S_ISREG) as mock_stat_S_ISREG, \
             mock.patch('uuid.uuid4', return_value='uuid4'), \
             mock.patch('sys.stderr.write', return_value=None) as mock_sys_stderr_write:
            contents = secure_read_file(full_file_path)
            self.assertIsNone(contents)
            calls = [
                mock.call(f'Warning: <geopm-service> {full_file_path} was discovered with invalid permissions, it will be renamed to {renamed_path}\n'),
                mock.call(f'Warning: <geopm-service> the wrong permissions were {oct(expected_mode)}\n')
            ]
            mock_sys_stderr_write.assert_has_calls(calls)
            mock_os_path_exists.assert_called_once_with(full_file_path)
            mock_os_path_isdir.assert_called_once_with(full_file_path)
            mock_os_path_islink.assert_called_once_with(full_file_path)
            # os.stat() is also called internally by system functions like maybe os.path.islink()
            mock_os_stat.assert_called()
            mock_stat_S_ISREG.assert_called_with(expected_mode)
        self.assertFalse(os.path.exists(full_file_path))
        self.assertTrue(os.path.exists(renamed_path))

    def test_read_file_bad_user_owner(self):
        """File to be securely read in has wrong user owner.

        Creates the geopm-service directory, and creates a regular file with wrong user owner within.
        Calls secure_read_file() with that file.

        """
        dir_path = f'{self._TEMP_DIR.name}/geopm-service'
        os.mkdir(dir_path, mode=0o700)
        self.check_dir_perms(dir_path)
        file_name = "stuff.json"
        full_file_path = os.path.join(dir_path, file_name)
        renamed_path = f'{full_file_path}-uuid4-INVALID'
        # Create the full_file_path
        filename = Path(full_file_path)
        filename.touch(mode=0o600, exist_ok=True)

        file_mock = mock.create_autospec(os.stat_result, spec_set=True)
        file_mock.st_uid = os.getuid() + 1
        file_mock.st_gid = os.getgid()
        file_mock.st_mode = 0o600

        with mock.patch('os.path.exists', wraps=os.path.exists) as mock_os_path_exists, \
             mock.patch('os.path.isdir', wraps=os.path.isdir) as mock_os_path_isdir, \
             mock.patch('os.path.islink', wraps=os.path.islink) as mock_os_path_islink, \
             mock.patch('os.stat', return_value=file_mock) as mock_os_stat, \
             mock.patch('stat.S_ISREG', return_value=True) as mock_stat_S_ISREG, \
             mock.patch('uuid.uuid4', return_value='uuid4'), \
             mock.patch('sys.stderr.write', return_value=None) as mock_sys_stderr_write:
            contents = secure_read_file(full_file_path)
            self.assertIsNone(contents)
            calls = [
                mock.call(f'Warning: <geopm-service> {full_file_path} was discovered with invalid permissions, it will be renamed to {renamed_path}\n'),
                mock.call(f'Warning: <geopm-service> the wrong user owner was {file_mock.st_uid}\n')
            ]
            mock_sys_stderr_write.assert_has_calls(calls)
            mock_os_path_exists.assert_called_once_with(full_file_path)
            mock_os_path_isdir.assert_called_once_with(full_file_path)
            mock_os_path_islink.assert_called_once_with(full_file_path)
            # os.stat() is also called internally by system functions like maybe os.path.islink()
            mock_os_stat.assert_called()
            mock_stat_S_ISREG.assert_called_with(file_mock.st_mode)
        self.assertFalse(os.path.exists(full_file_path))
        self.assertTrue(os.path.exists(renamed_path))

    def test_read_file_bad_group_owner(self):
        """File to be securely read in has wrong group owner.

        Creates the geopm-service directory, and creates a regular file with wrong group owner within.
        Calls secure_read_file() with that file.

        """
        dir_path = f'{self._TEMP_DIR.name}/geopm-service'
        os.mkdir(dir_path, mode=0o700)
        self.check_dir_perms(dir_path)
        file_name = "stuff.json"
        full_file_path = os.path.join(dir_path, file_name)
        renamed_path = f'{full_file_path}-uuid4-INVALID'
        # Create the full_file_path
        filename = Path(full_file_path)
        filename.touch(mode=0o600, exist_ok=True)

        file_mock = mock.create_autospec(os.stat_result, spec_set=True)
        file_mock.st_uid = os.getuid()
        file_mock.st_gid = os.getgid() + 1
        file_mock.st_mode = 0o600 | stat.S_IFREG

        with mock.patch('os.path.exists', wraps=os.path.exists) as mock_os_path_exists, \
             mock.patch('os.path.isdir', wraps=os.path.isdir) as mock_os_path_isdir, \
             mock.patch('os.path.islink', wraps=os.path.islink) as mock_os_path_islink, \
             mock.patch('os.stat', return_value=file_mock) as mock_os_stat, \
             mock.patch('stat.S_ISREG', wraps=stat.S_ISREG) as mock_stat_S_ISREG, \
             mock.patch('uuid.uuid4', return_value='uuid4'), \
             mock.patch('sys.stderr.write', return_value=None) as mock_sys_stderr_write:
            contents = secure_read_file(full_file_path)
            self.assertIsNone(contents)
            calls = [
                mock.call(f'Warning: <geopm-service> {full_file_path} was discovered with invalid permissions, it will be renamed to {renamed_path}\n'),
                mock.call(f'Warning: <geopm-service> the wrong group owner was {file_mock.st_gid}\n')
            ]
            mock_sys_stderr_write.assert_has_calls(calls)
            mock_os_path_exists.assert_called_once_with(full_file_path)
            mock_os_path_isdir.assert_called_once_with(full_file_path)
            mock_os_path_islink.assert_called_once_with(full_file_path)
            # os.stat() is also called internally by system functions like maybe os.path.islink()
            mock_os_stat.assert_called()
            mock_stat_S_ISREG.assert_called_with(file_mock.st_mode)
        self.assertFalse(os.path.exists(full_file_path))
        self.assertTrue(os.path.exists(renamed_path))

    def test_read_valid_file(self):
        """Opens and reads in a valid file which passes all checks.

        Creates the geopm-service directory, and creates a regular file within, and write the contents to it.
        Calls secure_read_file() with that file, verifying that the contents match.

        """
        dir_path = f'{self._TEMP_DIR.name}/geopm-service'
        os.mkdir(dir_path, mode=0o700)
        self.check_dir_perms(dir_path)
        file_name = "stuff.json"
        full_file_path = os.path.join(dir_path, file_name)
        input_contents = """Love is patient, love is kind.
        It does not envy, it does not boast, it is not proud.
        1 Corinthians 13:4
        """
        # Create the full_file_path, and write the contents into the file.
        with open(os.open(full_file_path, os.O_CREAT | os.O_WRONLY, 0o600), 'w') as file:
            file.write(input_contents)
        expected_mode = 0o600 | stat.S_IFREG

        with mock.patch('os.path.exists', wraps=os.path.exists) as mock_os_path_exists, \
             mock.patch('os.path.isdir', wraps=os.path.isdir) as mock_os_path_isdir, \
             mock.patch('os.path.islink', wraps=os.path.islink) as mock_os_path_islink, \
             mock.patch('os.stat', wraps=os.stat) as mock_os_stat, \
             mock.patch('stat.S_ISREG', wraps=stat.S_ISREG) as mock_stat_S_ISREG, \
             mock.patch('uuid.uuid4', return_value='uuid4'):
            output_contents = secure_read_file(full_file_path)
            self.assertEqual(input_contents, output_contents)
            mock_os_path_exists.assert_called_once_with(full_file_path)
            mock_os_path_isdir.assert_called_once_with(full_file_path)
            mock_os_path_islink.assert_called_once_with(full_file_path)
            # os.stat() is also called internally by system functions like maybe os.path.islink()
            mock_os_stat.assert_called()
            mock_stat_S_ISREG.assert_called_with(expected_mode)

    def test_secure_make_file(self):
        """Opens and reads in a valid file which passes all checks.

        Creates the geopm-service directory, and creates a regular file within, and write the contents to it.
        Calls secure_read_file() with that file, verifying that the contents match.

        """
        dir_path = f'{self._TEMP_DIR.name}/geopm-service'
        os.mkdir(dir_path, mode=0o700)
        self.check_dir_perms(dir_path)
        file_name = "stuff.json"
        full_file_path = os.path.join(dir_path, file_name)
        temp_path = f'{full_file_path}-uuid4-tmp'
        input_contents = """Love is patient, love is kind.
        It does not envy, it does not boast, it is not proud.
        1 Corinthians 13:4
        """

        with mock.patch('uuid.uuid4', return_value='uuid4'):
            secure_make_file(full_file_path, input_contents)

        self.assertFalse(os.path.exists(temp_path))
        self.assertTrue(os.path.exists(full_file_path))
        self.check_file_perms(full_file_path)

        with open(full_file_path, "r") as file:
            output_contents = file.read()
            self.assertEqual(input_contents, output_contents)

if __name__ == '__main__':
    unittest.main()
