
import http.server
import threading
import urllib.parse
import time

import constants


#*******************
#automatically shutdown after 5 minutes if not completed
auto_shutdown_time = 60*5
#*******************


class AuthServer(http.server.HTTPServer):

    
    def __init__(self, port, callback, callback_params):
        http.server.HTTPServer.__init__(self, ('', port), RequestHandlerClass=AuthHandler)
        self.callback = callback
        self.callback_params = callback_params
        self.code_received = False
        self.schedule_shutdown(auto_shutdown_time)

    def start_new_thread(self):
        self.thread = threading.Thread(target=self.serve_forever, daemon=True)
        self.thread.start()
        
    def callback_complete(self, code):
        if not self.code_received:
            self.code_received = True
            self.callback(code, self.callback_params)
            
    def schedule_shutdown(self, pause_interval):
        thread = threading.Thread(target=self.shutdown_after_interval, 
            args=(pause_interval,), daemon=True)
        thread.start()
        
    def shutdown_after_interval(self, *args):
        pause_interval = args[0]
        time.sleep(pause_interval)
        self.shutdown()
    
        
    
class AuthHandler(http.server.BaseHTTPRequestHandler):
    
    def do_GET(self):
        try:
            o = urllib.parse.urlparse(self.path)
            params = urllib.parse.parse_qs(o.query)
            
            if 'error' in params:
                code = None
            elif 'code' in params:
                code = params['code'][0]
            else:
                return
        
            self.server.callback_complete(code)
        except: 
            pass
        
        try:
            self.send_page()
        except:
            pass
        
        
        self.server.schedule_shutdown(5)

        
    def send_page(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        path = constants.LOGIN_HTML_PATH
        html = open(path, 'rb')
        self.wfile.write(html.read())
#         self.wfile.close()
        html.close()
            
        
    def log_message(self, format, *args):
        return
    
    
    
    
    
    
    
    
    
    
    