import logging, traceback
logging.basicConfig(filename='logging.log', encoding='utf-8', level=logging.ERROR)

class LoggingHandler(object):

    def handle_exception(exc_message, exc_object):
        print(exc_message)
        tb_str = ''.join(traceback.format_exception(None, exc_object, exc_object.__traceback__))
        logging.error(exc_message + " " + tb_str)