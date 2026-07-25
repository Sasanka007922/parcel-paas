import sys
import enum
from datetime import datetime
from pathlib import Path
import threading
import traceback

class LogLevel(enum.IntEnum):
    DEBUG=10
    INFO=20
    WARNING=30
    ERROR=40
    FATAL=50

class Logger:
    def __init__(self, name: str="parcel-paas", min_level: LogLevel=LogLevel.INFO):
        self.name=name
        self.min_level=min_level
        

        base_dir=Path(__file__).resolve().parent.parent
        logs_dir=base_dir / "logs"
        logs_dir.mkdir(parents=True,exist_ok=True)

        date_str=datetime.now().strftime("%Y-%m-%d")
        self.log_file=logs_dir / f"{date_str}.log"
        self.file_lock = threading.Lock()


    def _log(self, level: LogLevel, msg:str, *args):
        if level<self.min_level:
            return
        if args:
            try:
                formatted_msg = msg%args
            except Exception:
                formatted_msg = msg
        else:
            formatted_msg=msg
        
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        log_line=f"[{timestamp}] [{level.name:<7}] [{self.name}] {formatted_msg}\n"

        out_stream=sys.stderr if level >= LogLevel.ERROR else sys.stdout
        out_stream.write(log_line)
        out_stream.flush()
        
        with self.file_lock:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(log_line)
            
    def debug(self,msg:str, *args):
        self._log(LogLevel.DEBUG, msg, *args)
    
    def info(self,msg:str, *args):
        self._log(LogLevel.INFO, msg, *args)

    def warning(self,msg:str, *args):
        self._log(LogLevel.WARNING, msg, *args)
    
    def error(self,msg:str, *args):
        self._log(LogLevel.ERROR, msg, *args)
    
    def fatal(self,msg:str, *args):
        self._log(LogLevel.FATAL, msg, *args)
    
    def exception(self, msg: str, *args):
        exc_type, exc_value, tb = sys.exc_info()
        
        if exc_type is not None:
            traceback_text = "".join(traceback.format_exception(exc_type, exc_value, tb))
        else:
            traceback_text = "No active exception context found.\n"

        formatted_msg = msg % args if args else msg

        full_msg = f"{formatted_msg}\n{traceback_text}"

        self._log(LogLevel.ERROR, full_msg)

logger=Logger()
    