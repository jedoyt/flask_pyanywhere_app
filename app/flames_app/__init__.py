from flask import render_template, Blueprint, request
from app.flames_app.flames_match import match_results


bp = Blueprint('flames_app',__name__)\

@bp.route('/flames_app', methods=['GET','POST'])
def matchmake():
  results = ""
  if request.method == 'POST':
    your_name = request.form['your-name']
    crush_name = request.form['crush-name']
    if your_name != '' and crush_name != '':
      results_header = f"{your_name} and {crush_name}"
      results = match_results(yourName=your_name, crushName=crush_name)
      return render_template('flames_app/flames_app.html', results_header=results_header, results=results)
    elif your_name == '' or crush_name == '':
      results_header = ""
      results = "Please complete name inputs"
      return render_template('flames_app/flames_app.html', results_header=results_header, results=results)
  
  return render_template('flames_app/flames_app.html', results=results)