from flask_wtf import Form
from wtforms import StringField, SubmitField, IntegerField, SelectField, DecimalField, BooleanField, TextAreaField, ValidationError
from wtforms.validators import Required, Optional
from wtforms.ext.dateutil.fields import DateField
from wtforms.fields.html5 import DateField
from ..models import Mood, Script

class DrugForm(Form):
    drug=SelectField('Drug', choices=[('Abilify', 'Abilify'), ('Ativan', 'Ativan'), ('Carbolith', 'Carbolith'), ('Celexa', 'Celexa'), ('Clozaril', 'Clozaril'), 
    	('Cymbalta', 'Cymbalta'), ('Depakine', 'Depakine'), ('Effexor', 'Effexor'), ('Gabapentin', 'Gabapentin'), ('Geodon', 'Geodon'), 
    	('Invega', 'Invega'), ('Klonopin', 'Klonopin'), ('Lamictal', 'Lamictal'), ('Lexapro', 'Lexapro'), ('Librium', 'Librium'), 
    	('Marplan', 'Marplan'), ('Mogadon', 'Mogadon'), ('Nardil', 'Nardil'), ('nipolept', 'Nipolept'), ('Parnate', 'Parnate'), ('Paxil', 'Paxil'), 
    	('Pregabalin', 'Pregabalin'), ('Prozac', 'Prozac'), ('Remeron', 'Remeron'), ('Risperdal', 'Risperdal'), ('Seroquel', 'Seroquel'), 
    	('Seroxat', 'Seroxat'), ('Tegretol', 'Tegretol'), ('Topiramate', 'Topiramate'), ('Trileptal', 'Trileptal'), ('Trintellix', 'Trintellix'), 
    	('Valium', 'Valium'), ('Vyvanse', 'Vyvanse'), ('Wellbutrin', 'Wellbutrin'), ('Xanax', 'Xanax'), ('Zoloft', 'Zoloft'), ('Zyprexa', 'Zyprexa')], validators=[Required()])
    dose=DecimalField('Dose (mg)', validators=[Required()])
    start = DateField('When did you start taking this medication?', validators=[Required()])
    end_date = DateField('When did you stop taking this medication? (Leave blank if you are still taking it)', validators=[Optional()])
    side_effects = TextAreaField('What side effects have you experienced while taking this medication?')
    submit = SubmitField('Submit')

class MoodForm(Form):
    mood = SelectField('Mood', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')])
    date = DateField('Date', validators=[Required()])
    side_effects = TextAreaField('Are you feeling any side effects today?')
    notes = TextAreaField('Notes')
    submit = SubmitField('Submit')