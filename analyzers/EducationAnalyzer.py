import pandas as pd
import numpy as np
from typing import Dict, List
from employee import Employee


class EducationAnalyzer:
    """Handles all educational analytics tasks"""

    def __init__(self, employees: List[Employee]):
        self.employees = employees
        self.education_hierarchy = {
            'Среднее специальное': 1,  # Vocational/Technical
            'Высшее': 2,  # Bachelor's
            'Магистратура': 3,  # Master's
            'Кандидат наук': 4,  # PhD Candidate
            'Доктор наук': 5  # Doctor of Sciences
        }

    def calculate_education_distribution(self) -> Dict:
        """Make a distribution of employees by education level"""
        education_count = {}

        for emp in self.employees:
            education = emp.education
            if education not in education_count:
                education_count[education] = 0
            education_count[education] += 1

        total_employees = len(self.employees)

        result = {}
        for education, count in education_count.items():
            result[education] = {
                'count': count,
                'percentage': round(count / total_employees * 100, 1),
                'education_level': self.education_hierarchy[education],
                'english_translation': self._translate_education(education)
            }

        return dict(sorted(result.items(), key=lambda x: x[1]['education_level'], reverse=True))

    def _translate_education(self, education: str) -> str:
        """Translate Russian education levels to English"""
        translations = {
            'Среднее специальное': 'Vocational/Technical',
            'Высшее': 'Bachelor',
            'Магистратура': 'Master',
            'Кандидат наук': 'PhD Candidate',
            'Доктор наук': 'Doctor of Sciences'
        }
        return translations.get(education, education)

    def analyze_education_salary_correlation(self) -> Dict:
        """Determine the correlation between education and salary"""
        education_salaries = {}

        for emp in self.employees:
            education = emp.education
            if education not in education_salaries:
                education_salaries[education] = []
            education_salaries[education].append(emp.salary)

        # Calculate statistics
        result = {}
        for education, salaries in education_salaries.items():
            result[education] = {
                'education_level': self.education_hierarchy[education],
                'avg_salary': round(sum(salaries) / len(salaries)),
                'median_salary': round(np.median(salaries)),
                'min_salary': min(salaries),
                'max_salary': max(salaries),
                'salary_range': max(salaries) - min(salaries),
                'employee_count': len(salaries),
                'english_translation': self._translate_education(education)
            }

        # Calculate correlation
        education_levels = []
        avg_salaries = []

        for education, data in result.items():
            education_levels.append(data['education_level'])
            avg_salaries.append(data['avg_salary'])

        if len(education_levels) > 1:
            correlation = np.corrcoef(education_levels, avg_salaries)[0, 1]
        else:
            correlation = 0

        # Calculate salary premium for higher education
        base_salary = result.get('Среднее специальное', {}).get('avg_salary', 0)
        salary_premiums = {}
        for education, data in result.items():
            if base_salary > 0:
                premium = ((data['avg_salary'] - base_salary) / base_salary) * 100
                salary_premiums[education] = round(premium, 1)

        return {
            'education_salary_data': result,
            'correlation_coefficient': round(correlation, 3),
            'correlation_interpretation': self._interpret_correlation(correlation),
            'salary_premiums': salary_premiums,
            'educationROI': self._calculate_education_roi(result)
        }

    def _interpret_correlation(self, correlation: float) -> str:
        """Interpret the correlation coefficient"""
        if correlation > 0.7:
            return "Strong positive correlation - higher education strongly correlates with higher salary"
        elif correlation > 0.3:
            return "Moderate positive correlation - education level significantly affects salary"
        elif correlation > 0:
            return "Weak positive correlation - slight relationship between education and salary"
        elif correlation == 0:
            return "No correlation - education level doesn't affect salary"
        else:
            return "Negative correlation - unexpected inverse relationship"

    def _calculate_education_roi(self, education_data: Dict) -> Dict:
        """Calculate return on investment for education"""
        base_salary = education_data.get('Среднее специальное', {}).get('avg_salary', 0)
        roi_data = {}

        for education, data in education_data.items():
            if education != 'Среднее специальное' and base_salary > 0:
                salary_difference = data['avg_salary'] - base_salary
                roi_data[education] = {
                    'salary_difference': salary_difference,
                    'roi_percentage': round((salary_difference / base_salary) * 100, 1),
                    'annual_premium': salary_difference * 12
                }

        return roi_data

    def find_departments_with_higher_education(self) -> Dict:
        """Find the departments with the largest number of employees with higher education"""
        higher_education = ['Магистратура', 'Кандидат наук', 'Доктор наук']
        department_education = {}

        for emp in self.employees:
            dept = emp.department_name
            if dept not in department_education:
                department_education[dept] = {'total': 0, 'higher_ed': 0}

            department_education[dept]['total'] += 1
            if emp.education in higher_education:
                department_education[dept]['higher_ed'] += 1

        result = {}
        for dept, data in department_education.items():
            higher_ed_percentage = (data['higher_ed'] / data['total']) * 100
            result[dept] = {
                'total_employees': data['total'],
                'higher_education_count': data['higher_ed'],
                'higher_education_percentage': round(higher_ed_percentage, 1),
                'classification': self._classify_education_level(higher_ed_percentage)
            }

        return dict(sorted(result.items(), key=lambda x: x[1]['higher_education_percentage'], reverse=True))

    def _classify_education_level(self, percentage: float) -> str:
        """Classify department education level"""
        if percentage >= 60:
            return "Elite Education"
        elif percentage >= 40:
            return "Highly Educated"
        elif percentage >= 20:
            return "Moderately Educated"
        else:
            return "Standard Education"

    def generate_education_report(self):
        """Generate comprehensive education analysis report"""
        print("=== EDUCATION ANALYSIS REPORT ===")

        # Education Distribution
        distribution = self.calculate_education_distribution()
        print(f"\n1. EDUCATION LEVEL DISTRIBUTION")
        total_employees = len(self.employees)
        for education, data in distribution.items():
            print(f"  {education} ({data['english_translation']}):")
            print(f"    Count: {data['count']} ({data['percentage']}%)")
            print(f"    Level: {data['education_level']}")

        # Education-Salary Correlation
        salary_corr = self.analyze_education_salary_correlation()
        print(f"\n2. EDUCATION-SALARY CORRELATION")
        print(f"Correlation Coefficient: {salary_corr['correlation_coefficient']}")
        print(f"Interpretation: {salary_corr['correlation_interpretation']}")

        print(f"\nSalary by Education Level:")
        for education, data in salary_corr['education_salary_data'].items():
            print(f"  {education}: {data['avg_salary']:,.0f} RUB (Level {data['education_level']})")

        # Higher Education Departments
        higher_ed_depts = self.find_departments_with_higher_education()
        print(f"\n3. DEPARTMENTS WITH HIGHEST HIGHER EDUCATION")
        top_5 = list(higher_ed_depts.items())[:5]
        for i, (dept, data) in enumerate(top_5, 1):
            print(f"  {i}. {dept}: {data['higher_education_percentage']}% ({data['classification']})")
            print(f"     {data['higher_education_count']}/{data['total_employees']} employees with higher education")

        return {
            'education_distribution': distribution,
            'education_salary_correlation': salary_corr,
            'higher_education_departments': higher_ed_depts
        }