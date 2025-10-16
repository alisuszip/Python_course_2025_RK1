import pandas as pd
from typing import Dict, List, Tuple
from employee import Employee


class DemographicAnalyzer:
    """Handles all demographic analysis tasks"""

    def __init__(self, employees: List[Employee]):
        self.employees = employees

    def calculate_gender_age_distribution(self) -> Dict:
        """Calculate the distribution of employees by gender and age"""
        gender_count = {'male': 0, 'female': 0}
        age_groups = {
            '18-25': {'male': 0, 'female': 0, 'total': 0},
            '26-35': {'male': 0, 'female': 0, 'total': 0},
            '36-45': {'male': 0, 'female': 0, 'total': 0},
            '46-55': {'male': 0, 'female': 0, 'total': 0},
            '56-65': {'male': 0, 'female': 0, 'total': 0},
            '65+': {'male': 0, 'female': 0, 'total': 0}
        }

        for emp in self.employees:
            # Count gender
            gender_count[emp.gender] += 1

            # Categorize by age
            age = emp.age
            if age <= 25:
                age_group = '18-25'
            elif age <= 35:
                age_group = '26-35'
            elif age <= 45:
                age_group = '36-45'
            elif age <= 55:
                age_group = '46-55'
            elif age <= 65:
                age_group = '56-65'
            else:
                age_group = '65+'

            age_groups[age_group][emp.gender] += 1
            age_groups[age_group]['total'] += 1

        total_employees = len(self.employees)

        return {
            'gender_distribution': {
                'count': gender_count,
                'percentage': {
                    'male': round(gender_count['male'] / total_employees * 100, 1),
                    'female': round(gender_count['female'] / total_employees * 100, 1)
                }
            },
            'age_gender_distribution': age_groups,
            'total_employees': total_employees
        }

    def calculate_average_age_by_department(self) -> Dict:
        """Determine the average age by department"""
        department_ages = {}

        for emp in self.employees:
            dept = emp.department_name
            if dept not in department_ages:
                department_ages[dept] = []
            department_ages[dept].append(emp.age)

        result = {}
        for dept, ages in department_ages.items():
            avg_age = sum(ages) / len(ages)
            result[dept] = {
                'average_age': round(avg_age, 1),
                'employee_count': len(ages),
                'min_age': round(min(ages), 1),
                'max_age': round(max(ages), 1),
                'age_range': round(max(ages) - min(ages), 1)
            }

        return dict(sorted(result.items(), key=lambda x: x[1]['average_age'], reverse=True))

    def find_gender_imbalance(self) -> Dict:
        """Find the departments with the greatest gender imbalance"""
        department_gender = {}

        for emp in self.employees:
            dept = emp.department_name
            if dept not in department_gender:
                department_gender[dept] = {'male': 0, 'female': 0}
            department_gender[dept][emp.gender] += 1

        result = {}
        for dept, genders in department_gender.items():
            total = genders['male'] + genders['female']
            male_percentage = (genders['male'] / total) * 100
            female_percentage = (genders['female'] / total) * 100
            imbalance_score = abs(male_percentage - 50)  # Distance from perfect balance

            result[dept] = {
                'male_count': genders['male'],
                'female_count': genders['female'],
                'total_employees': total,
                'male_percentage': round(male_percentage, 1),
                'female_percentage': round(female_percentage, 1),
                'imbalance_score': round(imbalance_score, 1),
                'status': 'Male-dominated' if male_percentage > 60 else 'Female-dominated' if female_percentage > 60 else 'Balanced'
            }

        sorted_result = dict(sorted(result.items(), key=lambda x: x[1]['imbalance_score'], reverse=True))

        # Find extremes
        most_imbalanced = list(sorted_result.items())[0] if sorted_result else (None, None)
        most_balanced = list(sorted_result.items())[-1] if sorted_result else (None, None)

        return {
            'department_imbalance': sorted_result,
            'most_imbalanced_department': most_imbalanced,
            'most_balanced_department': most_balanced,
            'summary': {
                'male_dominated_count': len([d for d in sorted_result.values() if d['male_percentage'] > 60]),
                'female_dominated_count': len([d for d in sorted_result.values() if d['female_percentage'] > 60]),
                'balanced_count': len([d for d in sorted_result.values() if 40 <= d['male_percentage'] <= 60])
            }
        }

    def generate_demographic_report(self):
        """Generate comprehensive demographic report"""
        print("=== DEMOGRAPHIC ANALYSIS REPORT ===")

        # Gender and Age Distribution
        gender_age = self.calculate_gender_age_distribution()
        print(f"\n1. GENDER AND AGE DISTRIBUTION")
        print(f"Total Employees: {gender_age['total_employees']}")
        print(f"Gender Distribution:")
        print(
            f"  Male: {gender_age['gender_distribution']['count']['male']} ({gender_age['gender_distribution']['percentage']['male']}%)")
        print(
            f"  Female: {gender_age['gender_distribution']['count']['female']} ({gender_age['gender_distribution']['percentage']['female']}%)")

        print(f"\nAge and Gender Distribution:")
        for age_group, data in gender_age['age_gender_distribution'].items():
            if data['total'] > 0:
                print(f"  {age_group}: {data['total']} employees (M: {data['male']}, F: {data['female']})")

        # Average Age by Department
        age_by_dept = self.calculate_average_age_by_department()
        print(f"\n2. AVERAGE AGE BY DEPARTMENT")
        for dept, data in list(age_by_dept.items())[:10]:  # Show top 10
            print(f"  {dept}: {data['average_age']} years ({data['employee_count']} employees)")

        # Gender Imbalance
        imbalance = self.find_gender_imbalance()
        print(f"\n3. GENDER IMBALANCE ANALYSIS")
        if imbalance['most_imbalanced_department'][0]:
            dept, data = imbalance['most_imbalanced_department']
            print(f"Most Imbalanced: {dept} (Score: {data['imbalance_score']})")
            print(
                f"  Male: {data['male_count']} ({data['male_percentage']}%), Female: {data['female_count']} ({data['female_percentage']}%)")

        print(f"\nSummary:")
        print(f"  Male-dominated departments: {imbalance['summary']['male_dominated_count']}")
        print(f"  Female-dominated departments: {imbalance['summary']['female_dominated_count']}")
        print(f"  Balanced departments: {imbalance['summary']['balanced_count']}")

        return {
            'gender_age_distribution': gender_age,
            'average_age_by_department': age_by_dept,
            'gender_imbalance': imbalance
        }