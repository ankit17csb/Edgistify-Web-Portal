from flask_wtf import Form
from wtforms import TextField, IntegerField, TextAreaField, SubmitField, RadioField,SelectField

from wtforms import validators, ValidationError

class adminWorks(Form):
   Table = RadioField('Table',[validators.Required("Please enter \
      your choice.")] , choices = [('fac','Faculty table'),('hod','Hod table'),
      ('crossC','Cross cutting table'),('leaveH','Leave hierarchy table')])
   
   
   Opt = SelectField('Operation', choices = [('I', 'Insert'), ('U', 'update'),('D','Delete')])
   submit = SubmitField("Send")

class facultyTable(Form):
    username = TextField("Name Of Faculty",[validators.Required("Please enter \
      name.")])
    
    dept = TextField("Name Of Dept",[validators.Required("Please enter \
      name.")])

    submit = SubmitField("Send")

class hodTable(Form):
    username = TextField("Name Of Hod",[validators.Required("Please enter \
      name.")])
    
    dept = TextField("Name Of Dept",[validators.Required("Please enter \
      name.")])

    submit = SubmitField("Send")

class crossCuttingTable(Form):
    username = TextField("Name Of CC",[validators.Required("Please enter \
      name.")])
    
    desgn = TextField("Name Of Desgn",[validators.Required("Please enter \
      name.")])

    submit = SubmitField("Send")

class leaveHTable(Form):
    child = TextField("Name Of child",[validators.Required("Please enter child \
      name.")])
    
    parent = TextField("Name Of parent",[validators.Required("Please enter parent\
      name.")])
    
    forWhom = TextField("Name Of for whom",[validators.Required("Please enter for whom\
      name.")])

    submit = SubmitField("Send")