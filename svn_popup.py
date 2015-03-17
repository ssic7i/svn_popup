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


from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QSystemTrayIcon
import svn_popup_lib
import sys
import os
import ConfigParser
import io
import datetime

class MainWindow(QtGui.QMainWindow):

    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.trayIcon = QtGui.QSystemTrayIcon(QtGui.QIcon('icon.png'))
        self.trayIcon.show()

        #--------------------------------------------------------------
        # Read config file
        main_config_file = open('conf.cfg', 'r')
        main_config_source = main_config_file.read()
        main_config_file.close()

        main_config = ConfigParser.RawConfigParser()
        main_config.readfp(io.BytesIO(main_config_source))
        #--------------------------------------------------------------
        self.paths_to_search = []
        # Look and record paths
        for itm in main_config.items('paths'):
            par, val = itm
            val = val.strip('"')
            if os.path.exists(val):
                self.paths_to_search.append(val + '\n')
        self.paths_str = ''
        for itm in self.paths_to_search:
            self.paths_str = self.paths_str + itm
        #--------------------------------------------------------------

        self.trayIcon.showMessage('Looking started', 'paths: ' + str(self.paths_str), QSystemTrayIcon.Information, 5000)

        #set timer
        self.timer = QtCore.QTimer(self)
        update_interval = int(main_config.get('conf', 'update_interval'))
        self.timer.setInterval(update_interval * 1000)
        self.timer.timeout.connect(self.run_app)
        self.timer.start()

        # set first tooltip
        self.trayIcon.setToolTip('paths: '  + str(self.paths_str))

        exitAction = QtGui.QAction('&Exit', self)
        exitAction.triggered.connect(self.closeEvent)

        show_message_Action = QtGui.QAction('&Show paths', self)
        show_message_Action.triggered.connect(self.show_message)

        menu = QtGui.QMenu(self)
        menu.addAction(exitAction)
        menu.addAction(show_message_Action)
        self.trayIcon.setContextMenu(menu)

    def run_app(self):

        far_paths = ''

        for c_path in self.paths_to_search:
            c_rev, c_mess = svn_popup_lib.get_cur_revision(c_path)
            h_rev, h_mess = svn_popup_lib.get_head_revision(c_path)

            if (c_rev is not None) and (h_rev is not None):
                if int(c_rev) != int(h_rev):
                    far_paths = far_paths + c_path + '\n'
            else:
                err_log = open('err.log', 'a')
                err_log.write('--------------------\n')
                err_log.write(str(datetime.datetime.now()) + '\n')
                err_log.write(c_mess.replace('[def]',''))
                err_log.write('--------------------\n')
                err_log.write(h_mess.replace('[def]',''))
                err_log.write('--------------------\n')
                err_log.close()


        if far_paths != '':
            self.trayIcon.showMessage('Not up to date', 'paths: ' + far_paths, QSystemTrayIcon.Information, 5000)
            self.trayIcon.setToolTip(far_paths)


    def show_message(self):
        self.trayIcon.showMessage('Looking paths', 'paths: '  + str(self.paths_str), QSystemTrayIcon.Information, 5000)

    # http://stackoverflow.com/questions/5506781/pyqt4-application-on-windows-is-crashing-on-exit
    def closeEvent(self, event):
        sys.exit(0)


app = QtGui.QApplication(sys.argv)
w = MainWindow()
#w.show()
sys.exit(app.exec_())