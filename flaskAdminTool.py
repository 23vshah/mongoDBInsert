from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

# Sample data for testing
scraper_data = [{'category': 'Prescribed Courses', 'type': 'P', 'grade': False, 'metric_type': None, 'metric_value': None, 'courses': ['IE 312', 'MATH 231', 'MATSE 259', 'ME 390', 'ME 490']}, {'category': 'Additional Courses', 'type': 'or', 'grade': False, 'metric_type': None, 'metric_value': None, 'courses': ['CMPSC 200', 'CMPSC 201']}, {'category': 'Additional Courses', 'type': 'or', 'grade': False, 'metric_type': None, 'metric_value': None, 'courses': ['ME 440W', 'ME 441W']}, {'category': 'Prescribed Courses: Require a grade of C or better', 'type': 'P', 'grade': True, 'metric_type': None, 'metric_value': None, 'courses': ['CHEM 110', 'EDSGN 100', 'EMCH 211', 'EMCH 212', 'EMCH 213', 'ENGL 202C', 'MATH 140', 'MATH 141', 'MATH 220', 'MATH 251', 'ME 300', 'ME 320', 'ME 330', 'ME 340', 'ME 348', 'ME 360', 'ME 370', 'ME 410', 'ME 435', 'ME 450', 'ME 454', 'PHYS 211', 'PHYS 212']}, {'category': 'Select 3 credits from the following: 0', 'type': 'seq', 'grade': False, 'metric_type': 'credits', 'metric_value': '3', 'courses': ['BIOL 141', 'BIOL 161', 'CHEM 111,PHYS 214', 'CHEM 112']}, {'category': 'Additional Courses: Require a grade of C or better', 'type': 'or', 'grade': True, 'metric_type': None, 'metric_value': None, 'courses': ['CAS 100A', 'CAS 100B']}, {'category': 'Additional Courses: Require a grade of C or better', 'type': 'or', 'grade': True, 'metric_type': None, 'metric_value': None, 'courses': ['ENGL 15', 'ENGL 30H']}, {'category': 'Select 3 credits from the following: 1', 'type': 'shortlist', 'grade': False, 'metric_type': 'credits', 'metric_value': '3', 'courses': ['ECON 14', 'ECON 102', 'ECON 104']}]


not_normal_courses = [
    "Not Normal Course: Select 1 credit of First-Year Seminar",
    "Not Normal Course: Select 3 credits in a 400-level ME Technical Elective course",
    "Not Normal Course: Select 6 credits in Engineering Technical Elective courses",
    "Not Normal Course: Select 3 credits in General Technical Elective courses"
]

@app.route('/')
def index():
    return render_template('adminTool.html', scraper_data=scraper_data, not_normal=not_normal_courses)

@app.route('/approve', methods=['POST'])
def approve_item():
    item_index = request.json.get('item')
    if item_index is not None and 0 <= item_index < len(scraper_data):
        approved_item = scraper_data[item_index]
        print("Approved item:", approved_item)  # Log the approved item
        return jsonify({'status': 'approved'})
    else:
        return jsonify({'status': 'error', 'message': 'Invalid item index'})


@app.route('/save_all', methods=['POST'])
def save_all():
    data = request.json.get('data')
    with open('approved_data.json', 'w') as f:
        json.dump(data, f, indent=4)
    return jsonify({'status': 'saved'})

if __name__ == "__main__":
    app.run(debug=True)
