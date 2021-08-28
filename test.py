from dotenv import load_dotenv
import os
from flask_mail import Mail, Message
from flask import Flask, flash, redirect, render_template, request, session, jsonify
load_dotenv()


# My app
app = Flask(__name__)

print(type(os.getenv("MAIL_USERNAME")))
print(type(os.getenv("MAIL_DEFAULT_SENDER")))
print(type(os.getenv("MAIL_PASSWORD")))