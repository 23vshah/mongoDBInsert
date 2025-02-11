from flask import Flask, render_template, request, redirect, url_for, jsonify
import json

app = Flask(__name__)

documents = []  # Store created documents here

# Type mapping for user input to JSON values
type_mapping = {
    "p": 1,  # prescribed
    "b": 2,  # biglist
    "sl": 3,  # short list
    "seq": 4,  # sequence
    "or": 5  # pick one
}

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', documents=documents)

@app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        # Collect form data
        document = {
            "_id": request.form.get("_id"),
            "type": int(request.form.get("type")),
            "grade": request.form.get("grade") == "on"
        }

        # Handle type-specific fields
        doc_type = request.form.get("type")

        if doc_type == "1":  # prescribed
            document["courses"] = request.form.get("courses", "").split(",") if request.form.get("courses") else []

        elif doc_type == "2":  # biglist
            document["list_names"] = request.form.get("list_names", "").split(",") if request.form.get("list_names") else []
            metric_type = int(request.form.get("metric_type"))
            document["metrics"] = {
                "Type": "Courses" if metric_type == 1 else "Credits",
                "Value": int(request.form.get("metric_value"))
            }
            excluded = request.form.get("exclude", "").split(",") if request.form.get("exclude") else []
            excluded_courses = request.form.get("excluded_courses", "").split(",") if request.form.get("excluded_courses") else []
            excluded.append(excluded_courses)
            document["exclude"] = excluded
            document["recommended"] = request.form.get("recommended", "").split(",") if request.form.get("recommended") else []

        elif doc_type == "3":  # short list
            metric_type = int(request.form.get("metric_type_shortlist"))
            print(request.form.get("metric_value_shortlist"), 1)
            document["metrics"] = {
                "Type": "Courses" if metric_type == 1 else "Credits",
                "Value": int(request.form.get("metric_value_shortlist"))
            }
            document["courses"] = request.form.get("courses_shortlist", "").split(",") if request.form.get("courses_shortlist") else []
            document["recommended"] = request.form.get("recommended_shortlist", "").split(",") if request.form.get("recommended_shortlist") else []

        elif doc_type == "4":  # sequence
            sequences = request.form.get("sequences", "").split(";") if request.form.get("sequences") else []
            document["sequences"] = [seq.split(",") for seq in sequences]

        elif doc_type == "5":  # pick one
            document["courses"] = request.form.get("courses_or", "").split(",") if request.form.get("courses_or") else []

        documents.append(document)
        return redirect(url_for('index'))

@app.route('/download')
def download():
    json_data = json.dumps(documents, indent=4)
    return jsonify(documents)




if __name__ == '__main__':
    app.run(debug=True)
