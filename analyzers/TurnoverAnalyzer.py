import pandas as pd
import numpy as np
from typing import Dict, List
from employee import Employee


class TurnoverAnalyzer:
    """Handles all turnover and flow analysis tasks"""

    def __init__(self, employees: List[Employee]):
        self.employees = employees

    def calculate_turnover_rates(self, tenure_threshold: float = 2.0) -> Dict:
        """Calculate the turnover rate for each department"""
        department_data = {}

        for emp in self.employees:
            dept = emp.department_name
            if dept not in department_data:
                department_data[dept] = {
                    'total': 0,
                    'short_tenure': 0,
                    'performance_scores': []
                }

            department_data[dept]['total'] += 1
            department_data[dept]['performance_scores'].append(emp.performance_score)

            if emp.tenure_years < tenure_threshold:
                department_data[dept]['short_tenure'] += 1

        result = {}
        for dept, data in department_data.items():
            turnover_rate = (data['short_tenure'] / data['total']) * 100
            avg_performance = sum(data['performance_scores']) / len(data['performance_scores'])

            result[dept] = {
                'total_employees': data['total'],
                'short_tenure_count': data['short_tenure'],
                'turnover_rate': round(turnover_rate, 1),
                'average_performance': round(avg_performance, 1),
                'average_tenure': self._get_avg_tenure(dept)
            }

        return dict(sorted(result.items(), key=lambda x: x[1]['turnover_rate'], reverse=True))

    def _get_avg_tenure(self, department: str) -> float:
        """Calculate average tenure for a department"""
        tenures = [emp.tenure_years for emp in self.employees if emp.department_name == department]
        return round(sum(tenures) / len(tenures), 1) if tenures else 0

    def identify_turnover_extremes(self) -> Dict:
        """Identify the departments with the highest and lowest turnover"""
        turnover_data = self.calculate_turnover_rates()

        if not turnover_data:
            return {}

        # Find extremes
        highest_turnover = max(turnover_data.items(), key=lambda x: x[1]['turnover_rate'])
        lowest_turnover = min(turnover_data.items(), key=lambda x: x[1]['turnover_rate'])

        # Get top and bottom 3
        sorted_turnover = sorted(turnover_data.items(), key=lambda x: x[1]['turnover_rate'], reverse=True)
        top_3_highest = sorted_turnover[:3]
        top_3_lowest = sorted_turnover[-3:]

        return {
            'highest_turnover': {
                'department': highest_turnover[0],
                'turnover_rate': highest_turnover[1]['turnover_rate'],
                'employee_count': highest_turnover[1]['total_employees'],
                'average_performance': highest_turnover[1]['average_performance']
            },
            'lowest_turnover': {
                'department': lowest_turnover[0],
                'turnover_rate': lowest_turnover[1]['turnover_rate'],
                'employee_count': lowest_turnover[1]['total_employees'],
                'average_performance': lowest_turnover[1]['average_performance']
            },
            'top_3_highest': [{'department': dept, 'rate': data['turnover_rate']} for dept, data in top_3_highest],
            'top_3_lowest': [{'department': dept, 'rate': data['turnover_rate']} for dept, data in top_3_lowest],
            'turnover_gap': highest_turnover[1]['turnover_rate'] - lowest_turnover[1]['turnover_rate']
        }

    def analyze_turnover_performance_relationship(self) -> Dict:
        """Analyze the relationship between turnover rate and performance_score"""
        turnover_data = self.calculate_turnover_rates()

        turnover_rates = []
        performance_scores = []
        departments = []

        for dept, data in turnover_data.items():
            turnover_rates.append(data['turnover_rate'])
            performance_scores.append(data['average_performance'])
            departments.append(dept)

        if len(turnover_rates) > 1:
            correlation = np.corrcoef(turnover_rates, performance_scores)[0, 1]
        else:
            correlation = 0

        # Categorize departments
        categories = {
            'high_turnover_low_performance': [],
            'high_turnover_high_performance': [],
            'low_turnover_high_performance': [],
            'low_turnover_low_performance': []
        }

        avg_turnover = np.mean(turnover_rates) if turnover_rates else 0
        avg_performance = np.mean(performance_scores) if performance_scores else 0

        for dept, data in turnover_data.items():
            if data['turnover_rate'] > avg_turnover and data['average_performance'] < avg_performance:
                categories['high_turnover_low_performance'].append(dept)
            elif data['turnover_rate'] > avg_turnover and data['average_performance'] >= avg_performance:
                categories['high_turnover_high_performance'].append(dept)
            elif data['turnover_rate'] <= avg_turnover and data['average_performance'] >= avg_performance:
                categories['low_turnover_high_performance'].append(dept)
            else:
                categories['low_turnover_low_performance'].append(dept)

        return {
            'correlation_coefficient': round(correlation, 3),
            'correlation_interpretation': self._interpret_correlation(correlation),
            'average_turnover_rate': round(avg_turnover, 1),
            'average_performance_score': round(avg_performance, 1),
            'department_categories': categories,
            'raw_data': list(zip(departments, turnover_rates, performance_scores))
        }

    def _interpret_correlation(self, correlation: float) -> str:
        """Interpret the correlation coefficient"""
        if correlation < -0.7:
            return "Strong negative correlation - higher turnover strongly correlates with lower performance"
        elif correlation < -0.3:
            return "Moderate negative correlation - turnover affects performance"
        elif correlation < 0:
            return "Weak negative correlation - slight relationship between turnover and performance"
        elif correlation == 0:
            return "No correlation - turnover doesn't affect performance"
        elif correlation < 0.3:
            return "Weak positive correlation"
        elif correlation < 0.7:
            return "Moderate positive correlation"
        else:
            return "Strong positive correlation"

    def generate_turnover_report(self):
        """Generate comprehensive turnover analysis report"""
        print("=== TURNOVER ANALYSIS REPORT ===")

        # Turnover Rates
        turnover_rates = self.calculate_turnover_rates()
        print(f"\n1. TURNOVER RATES BY DEPARTMENT (Tenure < 2 years)")
        for dept, data in list(turnover_rates.items())[:8]:  # Show top 8
            print(
                f"  {dept}: {data['turnover_rate']}% ({data['short_tenure_count']}/{data['total_employees']} employees)")

        # Turnover Extremes
        extremes = self.identify_turnover_extremes()
        print(f"\n2. TURNOVER EXTREMES")
        print(
            f"Highest Turnover: {extremes['highest_turnover']['department']} ({extremes['highest_turnover']['turnover_rate']}%)")
        print(
            f"Lowest Turnover: {extremes['lowest_turnover']['department']} ({extremes['lowest_turnover']['turnover_rate']}%)")
        print(f"Turnover Gap: {extremes['turnover_gap']:.1f} percentage points")

        # Turnover-Performance Relationship
        relationship = self.analyze_turnover_performance_relationship()
        print(f"\n3. TURNOVER-PERFORMANCE RELATIONSHIP")
        print(f"Correlation Coefficient: {relationship['correlation_coefficient']}")
        print(f"Interpretation: {relationship['correlation_interpretation']}")

        print(f"\nDepartment Categories:")
        for category, depts in relationship['department_categories'].items():
            print(f"  {category.replace('_', ' ').title()}: {len(depts)} departments")

        return {
            'turnover_rates': turnover_rates,
            'turnover_extremes': extremes,
            'turnover_performance_relationship': relationship
        }