#!/usr/bin/env python3
"""
A module to filter personal data fields in log messages.
"""

import re
import os
import logging
import mysql.connector
from typing import List
from mysql.connector import connection


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(
    fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """
    Replace occurrences of specified fields in a message with the redaction str
    """
    for field in fields:
        message = re.sub(f"(?<={field}=)[^{separator}]*", redaction, message)
    return message


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initialize the RedactingFormatter with fields to redact
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record, redacting sensitive fields
        """
        record.msg = filter_datum(
            self.fields, self.REDACTION, record.getMessage(), self.SEPARATOR
        )
        return super(RedactingFormatter, self).format(record)


def get_logger() -> logging.Logger:
    """
    Creates and returns a logger name 'user_data'
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    return logger


def get_db() -> connection.MySQLConnection:
    """
    Connects to a secure MySql db
    """
    db_username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    db_password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    db_host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME")

    db_connection = mysql.connector.connect(
        user=db_username, password=db_password, host=db_host, database=db_name
    )
    return db_connection

def main():
    """
    Main function to retrieve and display
    """
    db = get_db()
    logger = get_logger()
    cursor = db.cursor()

    query = "SELECT name, email, phone, ssn, password, ip, last_login, user_agent FROM users;"

    for row in cursor:
         message = f"name={row[0]}; email={row[1]}; phone={row[2]}; ssn={row[3]}; password={row[4]}; ip={row[5]}; last_login={row[6]}; user_agent={row[7]};"
         logger.info(message)

    cursor.close()
    db.close()

if __name__ == "__main__":
    main()

