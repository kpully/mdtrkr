from flask import render_template, redirect, request, url_for, flash
from . import main
from .forms import DrugForm, MoodForm
from .. import db
from .. models import User, Script, Mood
from datetime import datetime
from flask_login import login_required, current_user
from collections import defaultdict

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
def profile():
	return render_template('profile.html')

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/analysis')
def analysis():
	avg=0
	user=current_user._get_current_object()
	men = User.query.filter(User.gender=="Male", User.id!=user.id).all()
	women = User.query.filter(User.gender=="Female", User.id!=user.id).all()
	user_scripts = Script.query.filter_by(user=current_user._get_current_object())
	curr_scripts = []
	for s in user_scripts:
		if s.end_date:
			pass
		else:
			curr_scripts.append(s.start)
	max_ = max(curr_scripts)
	moods = Mood.query.filter(Mood.date>=max_, Mood.user_id==user.id).all()
	sum_=0
	divisor = 0
	for mood in moods:
		sum_ += mood.mood
		divisor += 1
	avg=float(sum_/divisor)
	female_scripts = defaultdict(set)
	male_scripts = defaultdict(set)
	user=current_user._get_current_object()
	for woman in women:
		try:
			female_scripts[Script.query.filter_by(user_id=woman.id).first().drug].add(Script.query.filter_by(user_id=woman.id).first().dose)
		except:
			pass
	for man in men:
		try:
			male_scripts[Script.query.filter_by(user_id=man.id).first().drug].add(Script.query.filter_by(user_id=man.id).first().dose)
		except:
			pass
	age_group = User.query.filter(User.age_group==user.age_group, User.id !=user.id).all()
	d = defaultdict(set)
	for person in age_group:
		try:
			d[Script.query.filter_by(user_id=person.id).first().drug].add(Script.query.filter_by(user_id=person.id).first().dose)
		except:
			pass
	return render_template('aggregate.html', male_scripts=male_scripts, female_scripts=female_scripts,  d=d, user_scripts=user_scripts, curr_scripts=curr_scripts, avg=avg)

@main.route('/moods')
def moods():
	moods = Mood.query.filter_by(user=current_user._get_current_object())
	return render_template('moods_graph.html', moods=moods)

@main.route('/prescriptions')
def prescriptions():
	scripts = Script.query.filter_by(user=current_user._get_current_object())
	return render_template('prescriptions.html', scripts=scripts)

@main.route('/education')
def education():
	return render_template('education.html')

@main.route('/contact')
def contact():
	return render_template('contact.html')

@main.route('/user/')
def user():
	scripts = Script.query.filter_by(user=current_user._get_current_object())
	moods = Mood.query.filter_by(user=current_user._get_current_object())
	if user is None:
		return redirect(url_for('.index'))
	return render_template('profile.html', scripts=scripts, moods=moods, user=user)

@main.route('/delete/<int:id>')
def del_record(id):
	script = Script.query.filter_by(id=id).first()
	if script:
		db.session.delete(script)
	scripts = Script.query.filter_by(user=current_user._get_current_object())
	#return redirect(url_for('user', scripts=scripts, user=user))
	return render_template('prescriptions.html', scripts=scripts, user=user)

@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_record(id):
	script = Script.query.get_or_404(id)
	form =DrugForm()
	if form.validate_on_submit():
		db.session.delete(script)
		db.session.commit()
		form.drug.data = script.drug
		form.dose.data=script.dose
		form.start.data=script.start
		form.end_date.data=script.end_date
		form.side_effects.data=script.side_effects
		script = Script(drug=form.drug.data, dose=form.dose.data, start=form.start.data, end_date=form.end_date.data, side_effects=form.side_effects.data, user = current_user._get_current_object())
		db.session.add(script)
		db.session.commit()
		scripts=Script.query.filter_by(user=current_user._get_current_object())
		flash('Your prescription was successfully edited.')
		return render_template('profile.html', scripts=scripts, user=user)
	form.drug.data = script.drug
	form.dose.data=script.dose
	form.start.data=script.start
	form.end_date.data=script.end_date
	form.side_effects.data=script.side_effects
	return render_template('edit_script.html', form=form)

@main.route('/add', methods=['GET', 'POST'])
def script():
	#script = Script.query.get_or_404(id)
	form = DrugForm()
	if form.validate_on_submit():
			script=Script(drug=form.drug.data, dose=form.dose.data, start=form.start.data, end_date=form.end_date.data, side_effects = form.side_effects.data, user= current_user._get_current_object())
			db.session.add(script)
			db.session.commit()
			flash('Your prescription was added successfully.')
			scripts = Script.query.all()
			return redirect(url_for('main.user'))
	return render_template('add_script.html', form=form)

@main.route('/mood', methods=['GET', 'POST'])
def mood():
	#script = Script.query.get_or_404(id)
	form = MoodForm()
	if form.validate_on_submit():
			mood=Mood(mood=form.mood.data, date=form.date.data, side_effects=form.side_effects.data, notes=form.notes.data, user= current_user._get_current_object())
			try:
				db.session.add(mood)
				db.session.commit()
			except:
   				session.rollback()
   				db.session.add(mood)
			flash('Your mood was recorded successfully.')
			return redirect(url_for('main.moods'))
	return render_template('add_script.html', form=form)


	#data
drugs_dict = {'Abilify': 'Atypical Antipsychotic','Ativan': 'Benzodiazapine','Clozaril': 'Atypical Antipsychotic', 'Cymbalta': 'SNRI','Depakote': 'Mood Stabilizer',
'Effexor': 'SNRI','Gabapentin': 'Mood Stabilizer','Geodon': 'Atypical Antipsychotic','Invega': 'Atypical Antipsychotic','Klonopin': 'Benzodiazapine',
 'Lamictal': 'Mood Stabilizer','Lexapro': 'SSRI','Librium': 'benzo','Lyrica': 'Mood Stabilizer','Nardil': 'MAOI','Parnate': 'MAOI', 'Paxil': 'SSRI',
 'Prozac': 'SSRI','Remeron': 'NASSA','Restoril': 'Benzodiazapine','Risperdal': 'Atypical Antipsychotic','Seroquel': 'Atypical Antipsychotic',
 'Tegretol': 'Mood Stabilizer','Topamax': 'Mood Stabilizer','Trileptal': 'Mood Stabilizer','Trintellix': 'atypical_antid','Valium': 'Benzodiazapine',
 'Wellbutrin': 'NDRI','Xanax': 'Benzodiazapine','Zoloft': 'SSRI','Zyprexa': 'Atypical Antipsychotic'}

