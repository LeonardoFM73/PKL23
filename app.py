from flask import Flask,render_template,url_for,request,session,logging,redirect,flash
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session,sessionmaker

from passlib.hash import sha256_crypt