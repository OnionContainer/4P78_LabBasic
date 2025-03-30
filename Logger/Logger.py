"""
Logger requirement:

0.A log includes:
content     timestamp   tag(s)  level   callstack

1.Global reachable singleton:
    1.def write(content:str, tags:List[str], level:LogLevel = LogLevel.PRINT)
    2.def read(tag, level:LogLevel = LogLevel.PRINT) -> List[str]

2.Load from old file:
    1.Load every files that are not archived
        with a limited load line or load time
    2.If no file for today, create a today file
    3.choose from day wise or week wise

3.HotArgument:
    When outer program is trying to get a HotArgument from Logger (),
"""
import os
from datetime import datetime
from enum import Enum
import traceback
from typing import List

import pandas
import pandas as pd
import ast

def hot(tag:str, default):
    return Logger.i().read_hot_argument(tag, default)

__Logger_Configer = {
    "HotArguments_Directory": "HotArguments",
}

class LogLevel(Enum):
    PRINT = 1
    LOG = 2
    ERROR = 3
    HOT_ARGUMENT = 4


class Logger:
    """
    Logger will load and save files from and to data/
    special filename: data/logs.csv
    """
    _instance = None

    @staticmethod
    def i():
        if Logger._instance is None:
            i = Logger()
            Logger._instance = i
            df = i.load("logs")
            if df is not None:
                i.load_logs(df)


        return Logger._instance

    
    def __init__(self) -> None:
        self.prints = pd.DataFrame(columns=["content", "timestamp", "tags", "level", "callstack"])
        self.logs = pd.DataFrame(columns=["content", "timestamp", "tags", "level", "callstack"])
        self.hot_arguments = pd.DataFrame(columns=["content", "timestamp", "tags", "level", "callstack"])
        self.hot_arguments = self.load("HotArguments")
        self.hot_arguments_edit_time = 0.0
        self.file_mapping = {
            LogLevel.PRINT: self.prints,
            LogLevel.LOG: self.logs,
            LogLevel.HOT_ARGUMENT: self.hot_arguments,
            LogLevel.ERROR: None,
        }
        self.AUTO_SAVE = True

    def _rebind_reference(self):
        self.file_mapping = {
            LogLevel.PRINT: self.prints,
            LogLevel.LOG: self.logs,
            LogLevel.HOT_ARGUMENT: self.hot_arguments,
            LogLevel.ERROR: None,
        }


    def load_logs(self, df:pd.DataFrame):
        self.logs = df

    def write(self, content: str, tags: List[str]=None, level: LogLevel = LogLevel.PRINT):
        log_entry = pd.DataFrame([{
            "content": content,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "tags": tags,
            "level": level.name,
            "callstack": "".join(traceback.format_stack())
        }])
        if level == LogLevel.PRINT:
            self.prints = pd.concat([self.prints, log_entry], ignore_index=True)
        elif level == LogLevel.LOG:
            self.logs = pd.concat([self.logs, log_entry], ignore_index=True)

        if self.AUTO_SAVE:
            self.save()

    def read_hot_argument(self, tag:str, default):
        """
        :param default:
        :param tag: the argument name to load
        :return: the string value of the argument
        """
        mtime = os.path.getmtime("data/HotArguments.csv")
        # print(f"time: {mtime}, {self.hot_arguments_edit_time}")
        if mtime != self.hot_arguments_edit_time:
            print("HotArgument changed, reloading...")
            self.hot_arguments = self.load("HotArguments")
            self.hot_arguments_edit_time = mtime
            self._rebind_reference()

        result = self.read(tag, LogLevel.HOT_ARGUMENT)
        if len(result) > 1:
            raise Exception(f"HotArgument {tag} found {len(result)} values, expected 1.")
        if len(result) == 0:
            """
            add a line to the current hot argument dataframe, store the key and default value. call save_dataframe_as to save it, and return default value.
            """
            new_row = pd.DataFrame([{
                "content": default,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "tags": [tag],
                "level": LogLevel.HOT_ARGUMENT.name,
                "callstack": "".join(traceback.format_stack())
            }])
            self.hot_arguments = pd.concat([self.hot_arguments, new_row], ignore_index=True)
            self.save_dataframe_as(self.hot_arguments, "HotArguments")
            return default
        return result[0]
        pass

    def read(self, tag: str = None, level: LogLevel = LogLevel.LOG, column:str|None='content'):
        """
        :param tag: the tag to look for(None means all)
        :param level: which log level(Default is LOG)
        :param column: which columns to look at(Default is 'content')
        :return: A list of content or a DataFrame
        """
        df = self.file_mapping[level]

        if tag is not None:#if None, user wants every row of data
            #Filter out all lines that does not contain the tag
            df = df[df["tags"].apply(lambda tags: tag in tags if tags else False)]

        if column is not None:#if None, user wants every column of data
            df = list(df[column])#if true, return the list instead of series

        return df

    def read_first(self, tag:str, level:LogLevel=LogLevel.PRINT):
        df = self.read(tag, level, 'content')
        if df.empty:
            return None
        return df.iloc[0]

    def save_dataframe_as(self, df:pandas.DataFrame, file_name:str):
        file_name = 'data/' + file_name + '.csv'
    
        try:
            df['tags'] = df['tags'].apply(lambda x: ",".join(x))
            df.to_csv(file_name, index=False)
        except FileNotFoundError:
            print(f"Directory for {file_name} not found. Please create the required directory.")


    def save(self):
        """
        save all current logs & prints to file
        prints  ->  data/*date*.csv
        logs    ->  data/logs.csv
        """
        date_string = datetime.now().strftime("%Y-%m-%d")
        file_name = 'data/' + date_string + '.csv'
        file_name_for_logs = 'data/logs.csv'
        try:
            self.prints.to_csv(file_name, index=False)
            self.logs.to_csv(file_name_for_logs, index=False)
        except FileNotFoundError:
            print(f"File {file_name} not found.")

    def load(self, file_name: str)->pd.DataFrame|None:
        """
        :param file_name: load data/file_name.csv(No need to specify directory and .xxx)
        :return: DataFrame or None
        """
        file_path = 'data/' + file_name + '.csv'

        try:
            df = pd.read_csv(file_path)
        except FileNotFoundError:
            print(f"File {file_path} not found.")
            return None

        # 将 tags 列的字符串转换为列表
        # print(df["tags"])
        df['tags'] = df['tags'].apply(lambda x: x.split(","))
        # df['tags'] = df['tags'].apply(lambda x: [x] if type(x) is str else x)
        # df['tags'] = df['tags'].apply(lambda x: [x] if isinstance(x, str) else ast.literal_eval(x))
        print(df.head(5))
        return df
###

def est_logger():
    logger = Logger.i()

    # 使用 Logger 的 write 方法写一些 log
    logger.write("Test1", ["tag1", "tag2"], LogLevel.PRINT)
    logger.write("Test2", ["tag3", "tag4"], LogLevel.PRINT)
    logger.write("Test3", ["_2", "_3"], LogLevel.LOG)
    logger.write("Test3", ["_2", "_4"], LogLevel.LOG)
    logger.write("Test3", ["_2", "_5"], LogLevel.LOG)
    logger.write("Test2", ["_2", "_6"], LogLevel.LOG)

    # 使用 Logger 的 read 方法读取带有 'tag1' 的 log

    logs_with_tag1 = logger.read()
    logs_with_tag1 = logs_with_tag1.drop(columns=["callstack"])
    # print(logs_with_tag1.head(5))
    # print(Logger.get_instance().load("2025-03-14").head(5).to_string())
    print(logger.read("_2", LogLevel.LOG).to_string())

# est_logger()

###