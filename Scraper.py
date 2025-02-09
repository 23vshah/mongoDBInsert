import requests
from bs4 import BeautifulSoup


def get_major_requirements(url: str):
    # Send a request to the provided URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code != 200:
        print("Failed to fetch the webpage.")
        return

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract the course list table
    course_table = soup.find('table', class_='sc_courselist')

    if not course_table:
        print("No course list table found.")
        return

    # Find all rows in the table
    rows = course_table.find_all('tr')

    courses = []  # Store course details
    current_category = None  # Track course category (e.g., Prescribed Courses)
    current_group = []  # Group courses by row parity
    previous_parity = None  # Keep track of previous row parity

    def add_current_group_to_courses():
        """Adds the current group to the courses list if not empty."""
        if current_group:
            courses.append(current_group[:])
            current_group.clear()


    count = 0
    # Iterate through the rows to extract course data
    for row in rows:
        # Check if it's a category header row
        category_header = row.find('span', class_='courselistcomment')
        if category_header:
            add_current_group_to_courses()
            headerText = category_header.text.strip()
            if "Prescribed" in headerText:
                current_category = category_header.text.strip()
            elif "Additional" in headerText:
                current_category = category_header.text.strip()
            elif "following:" in headerText:
                current_category = category_header.text.strip() + " " + str(count)
                count+=1
            elif "Supporting" in headerText:
                current_category = category_header.text.strip()
            else:
                current_group.append({
                    "Text Course": headerText
                })
                add_current_group_to_courses()
            continue

        # Extract course details
        columns = row.find_all('td')
        if len(columns) >= 2:
            code_tags = columns[0].find_all('a')

            if len(code_tags) == 1:
                code_tag = code_tags[0]
                course_code = code_tag.text.strip() if code_tag else "N/A"


                # Determine row parity based on the class of the first <td>
                class_attr = columns[0].parent.get('class', [])
                current_parity = 'even' if 'even' in class_attr else 'odd' if 'odd' in class_attr else 'unknown'

                # Group by parity with the previous row
                if previous_parity is not None and current_parity != previous_parity:
                    add_current_group_to_courses()

                # Append course details to the current group
                current_group.append({
                    "Category": current_category,
                    "Code": course_code,
                })

                previous_parity = current_parity
            else:
                andGroup = []
                for code_tag in code_tags:
                    course_code = code_tag.text.strip() if code_tag else "N/A"
                    andGroup.append(course_code)

                class_attr = columns[0].parent.get('class', [])
                current_parity = 'even' if 'even' in class_attr else 'odd' if 'odd' in class_attr else 'unknown'

                if previous_parity is not None and current_parity != previous_parity:
                    add_current_group_to_courses()

                current_group.append({
                    "Category": current_category,
                    "Code": andGroup,
                })

                previous_parity = current_parity



    # Add the last group
    add_current_group_to_courses()

    # Display the extracted courses grouped by row parity
    requirements = []
    current_category_to_reqs = ""
    courses_to_reqs = []
    for group in courses:
        # print("OR Group:")
        if len(group) == 1:
            for course in group:
                if 'Text Course' in course:
                    print(f"Not Normal Course: {course['Text Course']}")
                else:
                    # print( f"  Category: {course['Category']}, Code: {course['Code']}")
                    if course['Category'] != current_category_to_reqs:
                        if not courses_to_reqs:
                            current_category_to_reqs = course['Category']
                            courses_to_reqs.append(course['Code'])
                            continue
                        grade = False
                        type = ""
                        course_credits = None
                        course_credits_value = None

                        category = current_category_to_reqs
                        if "Prescribed" in category:
                            type = 'P'
                        elif "Select" in category:
                            type = "sel"
                            for x in courses_to_reqs:
                                if x is list:
                                    type = "seq"
                                    break
                                if "credits" in category:
                                    course_credits = 'credits'
                                else:
                                    course_credits = "courses"

                                course_credits_value = category[category.index('Select'):].split()[1].strip()

                        if "grade" in category:
                            if "grade of c or better" in category.lower():
                                grade = True
                            else:
                                print("Grade but not proper format: " + category)


                        obj = {'category': category, "type": type, 'grade': grade, 'course_credits': course_credits, 'course_credits_value': course_credits_value, 'courses': courses_to_reqs}
                        requirements.append(obj)
                        courses_to_reqs = []
                        current_category_to_reqs = course['Category']
                        courses_to_reqs.append(course['Code'])

                    else:
                        courses_to_reqs.append(course['Code'])
        else:
            grade = False

            category = group[0]['Category']

            if "grade" in category:
                if "grade of c or better" in category.lower():
                    grade = True
                else:
                    print("Grade but not proper format: " + category)

            type = 'or'
            courses = [course['Code'] for course in group]
            obj = {'category': category, "type": type, 'grade': grade, 'course_credits': None,
                   'course_credits_value': None, 'courses': courses}
            requirements.append(obj)





    return requirements


# Example usage (replace with the actual URL)
url = "https://bulletins.psu.edu/undergraduate/colleges/engineering/computer-science-bs/#programrequirementstext"
print(get_major_requirements(url))
