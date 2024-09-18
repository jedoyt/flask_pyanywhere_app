from flask import Blueprint, render_template, request
from app.ml_app_breast_cancer.ml_model import build_knn_model, knn_predict, cancer, convert_dataset_to_dict, get_summary_stats
import numpy as np


bp = Blueprint('ml_app_breast_cancer', __name__)


@bp.route('/breast_cancer_classifier', methods=['GET', 'POST'])
def index():
    cancer_dict = convert_dataset_to_dict(cancer=cancer)
    stats_dict = get_summary_stats(cancer_dict=cancer_dict)

    if request.method == 'POST':
        # Create instance of KNN Model
        knn_model = build_knn_model(n=10)
        inputs = list()
        
        # Collect inputs from form
        for name in list(stats_dict.keys()):
            if request.form[name] == '':
                inputs.append(stats_dict[name]['median'])
            else:    
                inputs.append(float(request.form[name]))
        
        # Prediction
        prediction = knn_predict(model=knn_model, X_arr=np.array(inputs).reshape(1,-1))

        return render_template(
        'ml_app_breast_cancer/breast_cancer_classifier.html', 
        stats_dict=list(stats_dict.items()), prediction=prediction
        )

    return render_template(
        'ml_app_breast_cancer/breast_cancer_classifier.html', 
        stats_dict=list(stats_dict.items())
        )

@bp.route('/breast_cancer_dataset_info', methods=['GET', 'POST'])
def dataset_info():
    return render_template('ml_app_breast_cancer/dataset_info.html')