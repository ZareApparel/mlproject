import logging #Logging is a Python library through which we can record errors, messages, and other stuff. We are importing that library here.
import os #Os is a Python module/library which helps us to work with files, directories, etc..
import sys
from datetime import datetime

LOG_FILE=f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log" #Now, here in LOG_FILE we are storing in variable (LOG_FILE) that how should be the name of our file path where we will be logging. It says that it will be like that first instance of that file path name would be datetime, the current date and time then .log will come. f string allows us to use both functions and string. datetime.now().strftime('%m_%d_%Y_%H_%M_%S') is a function and that is why it is put inside "{}" so that it is not counted as string. datetime.now() will generate current date and time and what .strftime('%m_%d_%Y_%H_%M_%S') does is that it says that current date and current time will be in ('%m_%d_%Y_%H_%M_%S') format, first month, then day, year, then hour, min, second! At the last of our file_path name .log will come.

# print(LOG_FILE)
logs_path=os.path.join(os.getcwd(), "logs")  #Now, here we made a new variable called logs_path. What it does? os.path.join means join folder with file or current directory with new folder. It is used because this os.path.join allows us to work in both windows and linux because different systems have different ways for syntax. Some uses os.getcwd()/"logs", some os.getcwd()\"logs". We could use just os.getcwd()/"logs" if we would have been working only in windows but since we used linux small system as well. os.path.join makes it safe. logs_path is just a variable that has said that there would be a folder names logs inside our current directory and os.getcwd() finds our current directory. And we store this path of logs folder inside our current directory in logs_path. This does not create logs folder inside our current directory, os.makedirs does that. It just says logs folder inside our current directory.

# print(logs_path)

os.makedirs(logs_path, exist_ok=True) # Now this is os.makedirs. It create is used to make directories/folders. Here, it says make a directory using logs_path variable. So what does logs_path variable has? It says logs folder inside our current directory. So what will os.makedirs do? It will create a logs folder inside our current directory. exist_ok=True says if already such folder exists, no need to make new. 

LOG_FILE_PATH=os.path.join(logs_path, LOG_FILE) #LOG_FILE_PATH is a variable which says LOG_FILE a file will be inside logs_path a folder. logs_path has logs folder and LOG_FILE has file. So, os.path.join joins both means our log_file will be inside logs folder. This path is stored inside LOG_FILE_PATH.


logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)  #This is our basic settings for logger.py. It says our file_name will be LOG_FILE_PATH. Ofc LOG_FILE_PATH stores address for our log_file, saying our log_file will be inside logs folder and lOG_FILE will have datetime.now() in start of name and at end there would be .log. Now it says at second line telling format of our log messages, that how would log messages will appear in LOG_FILE when we will write logging.info() to store messages. It says first instance will be asctime, current time, second instance will be lineno, line number, 3rd will be name which is ROOT, 4th level name which could be INFO, WARNING, etc.. but we will mostly use INFO and at last message which we wrote. In 3rd line, it says level is INFO, so except DEBUG we can use any other like INFO, WARNING, etc..



if __name__ == ('__main__'):
    logging.info('Logging has started')
