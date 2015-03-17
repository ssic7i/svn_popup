#Copyright 2015 Serhii Sheiko
#
#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.


import ConfigParser
import subprocess
import io

def get_svn_path():
    main_config_file = open('conf.cfg', 'r')
    main_config_source = main_config_file.read()
    main_config_file.close()

    main_config = ConfigParser.RawConfigParser()
    main_config.readfp(io.BytesIO(main_config_source))

    svn_path = main_config.get('conf', 'svn')
    return svn_path


def get_cur_revision(path_to_folder):

    PIPE = subprocess.PIPE
    command = get_svn_path() + ' info ' + path_to_folder
    k = subprocess.Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=subprocess.STDOUT)
    k.wait()
    s = k.stdout.read()
    s = '[def]\n' + s
    cur_rev = ''
    try:
        svn_rev = ConfigParser.RawConfigParser()
        svn_rev.readfp(io.BytesIO(s.lower()))
        cur_rev = svn_rev.get('def', 'Revision'.lower())
    except:
        cur_rev = 'error'
        return cur_rev, s
    return cur_rev, ''



def get_head_revision(path_to_folder):

    PIPE = subprocess.PIPE
    command = get_svn_path() + ' info -r HEAD ' + path_to_folder
    k = subprocess.Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=subprocess.STDOUT)
    k.wait()
    s = k.stdout.read()
    s = '[def]\n' + s
    cur_rev = ''
    try:
        svn_rev = ConfigParser.RawConfigParser()
        svn_rev.readfp(io.BytesIO(s.lower()))
        cur_rev = svn_rev.get('def', 'Revision'.lower())
    except:
        cur_rev = None
        return cur_rev, s
    return cur_rev, ''

#------Test's------
#main_config_file = open('conf.cfg', 'r')
#main_config_source = main_config_file.read()
#main_config_file.close()
#
#main_config = ConfigParser.RawConfigParser()
#main_config.readfp(io.BytesIO(main_config_source))
#
#folder_path = main_config.get('paths', 'path1')
#print(folder_path)
#rev, msg = get_head_revision(folder_path)
#if rev is not None:
#    print(rev)
#else:
#    print(msg)
#
#rev2, msg2 = get_cur_revision(folder_path)
#if rev is not None:
#    print(rev2)
#else:
#    print(msg2)
#
#print(rev == rev2)
