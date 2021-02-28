import win32serviceutil
import win32service
import win32event
import win32evtlogutil
import servicemanager
import win32timezone
import socket
from waitress.server import create_server
from waitress import serve
import os
import sys

from wsgi import app
from src.logger import logger

sys.path.append(os.path.dirname(__name__))


class WaitressServer:

    def __init__(self, host, port):
        self.server = create_server(app, host=host, port=port)

    # call this method from your service to start the Waitress server
    def run(self):
        self.server.run()

    # call this method from the services stop method
    def stop_service(self):
        self.server.close()


class Service(win32serviceutil.ServiceFramework):
    _svc_name_ = "PDFService"
    _svc_display_name_ = "Pdf-editor service"

    # def __init__(self, *args):
    #     win32serviceutil.ServiceFramework.__init__(self, *args)
    #     self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
    #     socket.setdefaulttimeout(5)
    #     self.stop_requested = False
    #     self.serve = WaitressServer('*', 8800)
    #
    # def SvcStop(self):
    #     self.serve.stop_service()
    #     self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
    #     win32event.SetEvent(self.hWaitStop)
    #     self.ReportServiceStatus(win32service.SERVICE_STOPPED)
    #     logger.info('Stopped service ...')
    #     self.stop_requested = True
    #
    # def SvcDoRun(self):
    #     servicemanager.LogMsg(
    #         servicemanager.EVENTLOG_INFORMATION_TYPE,
    #         servicemanager.PYS_SERVICE_STARTED,
    #         (self._svc_name_, '')
    #     )
    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)
        self.serve = WaitressServer('*', 8800)

    def SvcStop(self):
        self.serve.stop_service()
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.main()

    def main(self):
        self.serve.run()


def post_service_update(*args):
    import win32api, win32con, win32profile, pywintypes
    from contextlib import closing

    env_reg_key = "SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Environment"
    hkey = win32api.RegOpenKeyEx(win32con.HKEY_LOCAL_MACHINE, env_reg_key, 0, win32con.KEY_ALL_ACCESS)

    with closing(hkey):
        system_path = win32api.RegQueryValueEx(hkey, 'PATH')[0]
        # PATH may contain %SYSTEM_ROOT% or other env variables that must be expanded
        # ExpandEnvironmentStringsForUser(None) only expands System variables
        system_path = win32profile.ExpandEnvironmentStringsForUser(None, system_path)
        system_path_list = system_path.split(os.pathsep)

        core_dll_file = win32api.GetModuleFileName(sys.dllhandle)
        core_dll_name = os.path.basename(core_dll_file)
        for search_path_dir in system_path_list:
            try:
                dll_path = win32api.SearchPath(search_path_dir, core_dll_name)[0]
                print(f"System python DLL: {dll_path}")
                break
            except pywintypes.error as ex:
                if ex.args[1] != 'SearchPath': raise
                continue
        else:
            print("*** WARNING ***")
            print(f"Your current Python DLL ({core_dll_name}) is not in your SYSTEM PATH")
            print("The service is likely to not launch correctly.")

    from win32serviceutil import LocatePythonServiceExe
    pythonservice_exe = LocatePythonServiceExe()
    pywintypes_dll_file = pywintypes.__spec__.origin

    pythonservice_path = os.path.dirname(pythonservice_exe)
    pywintypes_dll_name = os.path.basename(pywintypes_dll_file)

    try:
        return win32api.SearchPath(pythonservice_path, pywintypes_dll_name)[0]
    except pywintypes.error as ex:
        if ex.args[1] != 'SearchPath': raise
        print("*** WARNING ***")
        print(f"{pywintypes_dll_name} is not is the same directory as pythonservice.exe")
        print(f'Copy "{pywintypes_dll_file}" to "{pythonservice_path}"')
        print("The service is likely to not launch correctly.")

#
# if __name__ == '__main__':
#     win32serviceutil.HandleCommandLine(Service, customOptionHandler=post_service_update)


# if __name__ == '__main__':
#     if len(sys.argv) > 1:
#         # Called by Windows shell. Handling arguments such as: Install, Remove, etc.
#         win32serviceutil.HandleCommandLine(Service)
#     else:
#         # Called by Windows Service. Initialize the service to communicate with the system operator
#         servicemanager.Initialize()
#         servicemanager.PrepareToHostSingle(Service)
#         servicemanager.StartServiceCtrlDispatcher()


class SMWinservice(win32serviceutil.ServiceFramework):
    '''Base class to create winservice in Python'''

    _svc_name_ = "PDFService"
    _svc_display_name_ = "Pdf-editor service"
    _svc_description_ = 'Pdf-editor service'

    @classmethod
    def parse_command_line(cls):
        '''
        ClassMethod to parse the command line
        '''
        win32serviceutil.HandleCommandLine(cls)

    def __init__(self, args):
        '''
        Constructor of the winservice
        '''
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)

    def SvcStop(self):
        '''
        Called when the service is asked to stop
        '''
        self.stop()
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        '''
        Called when the service is asked to start
        '''
        self.start()
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.main()

    def start(self):
        '''
        Override to add logic before the start
        eg. running condition
        '''
        pass

    def stop(self):
        '''
        Override to add logic before the stop
        eg. invalidating running condition
        '''
        pass

    def main(self):
        '''
        Main class to be ovverridden to add logic
        '''
        pass


class PythonCornerExample(SMWinservice):
    _svc_name_ = "PDFService"
    _svc_display_name_ = "Pdf-editor service"
    _svc_description_ = 'Pdf-editor service'
    serve = WaitressServer('*', 8800)

    def start(self):
        self.serve.stop_service()

    def stop(self):
        self.serve.run()

    def main(self):
        pass


if __name__ == '__main__':
    PythonCornerExample.parse_command_line()