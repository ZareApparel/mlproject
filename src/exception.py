import sys
# Here we arr fetching sys which is a Python library that deals with errors when they happen

def er(error, error_detail:sys): #Here we made an er function where we give error example: division by zero and sys module so we can ask sys where error happened.
    _,_,exc_tb=error_detail.exc_info()
    #Here error_detail.exc_info asks sys where error happened, it returns 3 things where we don't need 1st 2 and 3rd one exc_tb gives exact location of where error happened. _ means ignore 1st, _ again ignores 2nd. 
    file_name=exc_tb.tb_frame.f_code.co_filename
    #In this file_name var exact file_name of where error happened will be stored.
    m="Error occured in Python script [{0}] line number [{1}] message [{2}]".format(file_name, exc_tb.tb_lineno, str(error))
    # Now in m var which is a message shows message that error happened in 3 empty slots and we will fill it with .format(in 1st one file.name, comes etc....)
    return m


class CustomException(Exception):
    #Here we are creating a class a child class which is inheriting from parent class Exception which is a built in Python class used to raise and except. We name this class as CustomException
    def __init__(self, error_message, error_detail:sys):
    #Here we do initialization with self, error_message and one error_detail:sys. When we will be doing using this class we will be writing here sys not error detail it is just a hint to tell Python that use sys module here to deal with error detail and in error_message we will write error message whatever it will be in parameter
        super().__init__(error_message)
    # Here we are calling parent class and activating it and making sure Python officially registers this as an error. 

        self.error_message=er(error_message, error_detail=error_detail)
    # Here we are adding our details on what will error_message show. Here we are calling function er which will return exact location of where error happened.

    def __str__(self):
        return self.error_message
    
# Now when we will print error it will show error message which called our function to tell exact location.