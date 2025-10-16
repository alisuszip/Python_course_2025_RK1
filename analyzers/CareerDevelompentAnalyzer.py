import pandas as pd
from typing import Dict, List
from employee import Employee


class CareerDevelopmentAnalyzer:
    """Handles all career development analysis tasks"""

    def __init__(self, employees: List[Employee]):
        self.employees = employees

    def analyze_team_lead_distribution(self) -> Dict:
        """Analyze the distribution of team lead positions by departments"""
        department_team_leads = {}

        for emp in self.employees:
            dept = emp.department_name
            if dept not in department_team_leads:
                department_team_leads[dept] = {'total': 0, 'team_leads': 0}

            department_team_leads[dept]['total'] += 1
            if emp.is_team_lead:
                department_team_leads[dept]['team_leads'] += 1

        result = {}
        for dept, data in department_team_leads.items():
            team_lead_ratio = (data['team_leads'] / data['total']) * 100
            result[dept] = {
                'total_employees': data['total'],
                'team_lead_count': data['team_leads'],
                'team_lead_ratio': round(team_lead_ratio, 1),
                'team_lead_density': round(data['total'] / max(data['team_leads'], 1), 1)  # Employees per team lead
            }

        return dict(sorted(result.items(), key=lambda x: x[1]['team_lead_ratio'], reverse=True))

    def calculate_average_promotion_time(self) -> Dict:
        """Determine the average time before promotion to team lead"""
        team_leads = [emp for emp in self.employees if emp.is_team_lead]

        if not team_leads:
            return {'average_tenure': 0, 'count': 0}

        tenures = [emp.tenure_years for emp in team_leads]
        experiences = [emp.experience_years for emp in team_leads]

        return {
            'average_tenure_to_promotion': round(sum(tenures) / len(tenures), 1),
            'average_experience_at_promotion': round(sum(experiences) / len(experiences), 1),
            'min_tenure': round(min(tenures), 1),
            'max_tenure': round(max(tenures), 1),
            'team_lead_count': len(team_leads),
            'tenure_distribution': self._categorize_tenure(tenures)
        }

    def _categorize_tenure(self, tenures: List[float]) -> Dict:
        """Categorize tenure into groups"""
        categories = {
            '0-2 years': 0,
            '2-5 years': 0,
            '5-10 years': 0,
            '10+ years': 0
        }

        for tenure in tenures:
            if tenure <= 2:
                categories['0-2 years'] += 1
            elif tenure <= 5:
                categories['2-5 years'] += 1
            elif tenure <= 10:
                categories['5-10 years'] += 1
            else:
                categories['10+ years'] += 1

        return categories

    def find_high_potential_employees(self, performance_threshold: float = 85.0) -> Dict:
        """Find employees with a high performance_score but without a team lead position"""
        high_potential = []

        for emp in self.employees:
            if (not emp.is_team_lead and
                    emp.performance_score >= performance_threshold and
                    emp.tenure_years >= 1.0):  # At least 1 year tenure

                high_potential.append({
                    'employee_id': emp.employee_id,
                    'name': f"{emp.first_name} {emp.last_name}",
                    'department': emp.department_name,
                    'position': emp.position,
                    'performance_score': emp.performance_score,
                    'tenure_years': round(emp.tenure_years, 1),
                    'experience_years': emp.experience_years,
                    'education': emp.education,
                    'salary': emp.salary,
                    'promotion_readiness': self._calculate_promotion_readiness(emp)
                })

        # Sort by performance score and tenure
        high_potential.sort(key=lambda x: (-x['performance_score'], -x['tenure_years']))

        # Group by department
        by_department = {}
        for emp in high_potential:
            dept = emp['department']
            if dept not in by_department:
                by_department[dept] = []
            by_department[dept].append(emp)

        return {
            'total_high_potential': len(high_potential),
            'high_potential_employees': high_potential[:20],  # Top 20
            'by_department': by_department,
            'department_summary': {dept: len(emps) for dept, emps in by_department.items()}
        }

    def _calculate_promotion_readiness(self, employee: Employee) -> str:
        """Calculate promotion readiness score"""
        score = 0

        # Performance (max 40 points)
        if employee.performance_score >= 90:
            score += 40
        elif employee.performance_score >= 80:
            score += 30
        elif employee.performance_score >= 70:
            score += 20
        else:
            score += 10

        # Tenure (max 30 points)
        if employee.tenure_years >= 3:
            score += 30
        elif employee.tenure_years >= 2:
            score += 20
        elif employee.tenure_years >= 1:
            score += 10

        # Experience (max 20 points)
        if employee.experience_years >= 10:
            score += 20
        elif employee.experience_years >= 5:
            score += 15
        elif employee.experience_years >= 2:
            score += 10
        else:
            score += 5

        # Education (max 10 points)
        education_points = {
            'Доктор наук': 10,
            'Кандидат наук': 9,
            'Магистратура': 8,
            'Высшее': 6,
            'Среднее специальное': 4
        }
        score += education_points.get(employee.education, 5)

        if score >= 80:
            return "Ready for promotion"
        elif score >= 60:
            return "Developing - 6-12 months"
        else:
            return "Needs development"

    def generate_career_development_report(self):
        """Generate comprehensive career development report"""
        print("=== CAREER DEVELOPMENT ANALYSIS REPORT ===")

        # Team Lead Distribution
        team_lead_dist = self.analyze_team_lead_distribution()
        print(f"\n1. TEAM LEAD DISTRIBUTION BY DEPARTMENT")
        for dept, data in list(team_lead_dist.items())[:8]:
            print(f"  {dept}: {data['team_lead_count']} team leads ({data['team_lead_ratio']}%)")
            print(f"    Density: 1 team lead per {data['team_lead_density']} employees")

        # Promotion Time Analysis
        promotion_time = self.calculate_average_promotion_time()
        print(f"\n2. AVERAGE TIME TO PROMOTION")
        print(f"Average Tenure to Team Lead: {promotion_time['average_tenure_to_promotion']} years")
        print(f"Average Experience at Promotion: {promotion_time['average_experience_at_promotion']} years")
        print(f"Team Lead Count: {promotion_time['team_lead_count']}")

        print(f"\nTenure Distribution at Promotion:")
        for category, count in promotion_time['tenure_distribution'].items():
            if count > 0:
                percentage = (count / promotion_time['team_lead_count']) * 100
                print(f"  {category}: {count} team leads ({percentage:.1f}%)")

        # High Potential Employees
        high_potential = self.find_high_potential_employees()
        print(f"\n3. HIGH POTENTIAL EMPLOYEES (Performance ≥ 85, Not Team Leads)")
        print(f"Total High Potential Employees: {high_potential['total_high_potential']}")

        print(f"\nTop 5 High Potential Employees:")
        for i, emp in enumerate(high_potential['high_potential_employees'][:5], 1):
            print(f"  {i}. {emp['name']} - {emp['department']}")
            print(f"     Performance: {emp['performance_score']}, Tenure: {emp['tenure_years']} years")
            print(f"     Position: {emp['position']}, Readiness: {emp['promotion_readiness']}")

        print(f"\nHigh Potential by Department:")
        for dept, count in list(high_potential['department_summary'].items())[:5]:
            print(f"  {dept}: {count} employees")

        return {
            'team_lead_distribution': team_lead_dist,
            'promotion_time_analysis': promotion_time,
            'high_potential_employees': high_potential
        }