import pandas as pd
from typing import Dict, List
from employee import Employee
from analyzers import TurnoverAnalyzer
from analyzers import CareerDevelompentAnalyzer


class HRStrategyAdvisor:
    """Handles all HR strategy and recommendations"""

    def __init__(self, employees: List[Employee]):
        self.employees = employees
        self.turnover_analyzer = TurnoverAnalyzer.TurnoverAnalyzer(employees)
        self.career_analyzer = CareerDevelompentAnalyzer.CareerDevelopmentAnalyzer(employees)

    def suggest_turnover_reduction_measures(self) -> Dict:
        """Suggest measures to reduce the turnover rate in problem departments"""
        turnover_data = self.turnover_analyzer.calculate_turnover_rates()

        # Identify problem departments (turnover > 25%)
        problem_departments = {dept: data for dept, data in turnover_data.items()
                               if data['turnover_rate'] > 25}

        measures = {}
        for dept, data in problem_departments.items():
            measures[dept] = {
                'current_turnover_rate': data['turnover_rate'],
                'employee_count': data['total_employees'],
                'average_tenure': data['average_tenure'],
                'average_performance': data['average_performance'],
                'immediate_actions': [
                    "Conduct stay interviews with current employees",
                    "Review and benchmark compensation packages",
                    "Implement mentorship program for new hires",
                    "Enhance onboarding process"
                ],
                'medium_term_strategies': [
                    "Develop clear career progression paths",
                    "Implement flexible work arrangements",
                    "Create departmental recognition programs",
                    "Provide professional development opportunities"
                ],
                'long_term_initiatives': [
                    "Build strong departmental culture",
                    "Develop leadership pipeline",
                    "Create cross-training opportunities",
                    "Implement succession planning"
                ],
                'specific_recommendations': self._get_department_specific_recommendations(dept, data)
            }

        return measures

    def _get_department_specific_recommendations(self, department: str, data: Dict) -> List[str]:
        """Get department-specific recommendations"""
        recommendations = []

        if 'разработк' in department.lower() or 'технич' in department.lower():
            recommendations.extend([
                "Provide latest tools and technologies",
                "Offer technical certification programs",
                "Create innovation time for personal projects",
                "Implement flexible remote work policies"
            ])
        elif 'продаж' in department.lower() or 'коммерч' in department.lower():
            recommendations.extend([
                "Review and optimize commission structures",
                "Provide advanced sales training",
                "Implement customer success metrics",
                "Create sales mentorship program"
            ])
        elif 'производств' in department.lower():
            recommendations.extend([
                "Improve safety and working conditions",
                "Implement performance-based bonuses",
                "Provide cross-training opportunities",
                "Create career progression in operations"
            ])
        else:
            recommendations.extend([
                "Conduct departmental satisfaction survey",
                "Review workload distribution",
                "Improve communication channels",
                "Provide departmental training budget"
            ])

        return recommendations

    def calculate_economic_effect(self, reduction_percent: float = 10) -> Dict:
        """Calculate the economic effect of reducing turnover by given percentage"""
        turnover_data = self.turnover_analyzer.calculate_turnover_rates()

        # Comprehensive cost model (in RUB)
        cost_components = {
            'recruitment': 50000,  # Recruitment agency fees, advertising
            'onboarding': 30000,  # Training, orientation, equipment
            'training': 40000,  # Formal training programs
            'productivity_loss': 70000,  # Ramp-up time, lost productivity
            'knowledge_loss': 10000,  # Institutional knowledge loss
            'manager_time': 20000  # Manager time for interviews, onboarding
        }

        avg_cost_per_turnover = sum(cost_components.values())

        total_turnover_cost = 0
        potential_savings = 0
        department_breakdown = {}

        for dept, data in turnover_data.items():
            current_turnover = data['short_tenure_count']
            dept_cost = current_turnover * avg_cost_per_turnover
            total_turnover_cost += dept_cost

            reduced_turnover = current_turnover * (1 - reduction_percent / 100)
            dept_savings = (current_turnover - reduced_turnover) * avg_cost_per_turnover
            potential_savings += dept_savings

            department_breakdown[dept] = {
                'current_turnover_cost': dept_cost,
                'potential_savings': dept_savings,
                'current_turnover_count': current_turnover,
                'reduced_turnover_count': reduced_turnover
            }

        # Calculate investment required (estimated at 15% of potential savings)
        investment_required = potential_savings * 0.15

        return {
            'current_annual_turnover_cost': round(total_turnover_cost),
            f'potential_savings_{reduction_percent}%_reduction': round(potential_savings),
            'required_investment': round(investment_required),
            'net_annual_savings': round(potential_savings - investment_required),
            'return_on_investment': round((potential_savings - investment_required) / investment_required * 100, 1),
            'payback_period_months': round(investment_required / (potential_savings / 12), 1),
            'cost_per_turnover': avg_cost_per_turnover,
            'department_breakdown': department_breakdown
        }

    def develop_high_potential_program(self) -> Dict:
        """Develop a development program for high-potential employees"""
        high_potential_data = self.career_analyzer.find_high_potential_employees()

        program = {
            'program_name': "Future Leaders Development Program",
            'target_audience': f"{high_potential_data['total_high_potential']} high-potential employees",
            'program_duration': '9 months',
            'program_phases': {
                'phase_1': {
                    'duration': '3 months',
                    'focus': 'Leadership Fundamentals',
                    'components': [
                        "Leadership assessment and 360 feedback",
                        "Communication and influence training",
                        "Strategic thinking workshops",
                        "Mentorship program kickoff"
                    ]
                },
                'phase_2': {
                    'duration': '3 months',
                    'focus': 'Applied Leadership',
                    'components': [
                        "Cross-departmental project assignment",
                        "Problem-solving simulations",
                        "Presentation skills development",
                        "Peer coaching circles"
                    ]
                },
                'phase_3': {
                    'duration': '3 months',
                    'focus': 'Strategic Impact',
                    'components': [
                        "Executive exposure and networking",
                        "Business case development",
                        "Change management training",
                        "Career path planning"
                    ]
                }
            },
            'selection_criteria': {
                'performance_threshold': 85,
                'minimum_tenure': 1,
                'leadership_potential': 'Based on manager recommendations',
                'education_preference': 'All levels considered'
            },
            'expected_outcomes': {
                'short_term': [
                    "30% promotion rate within 12 months",
                    "Improved employee engagement scores",
                    "Enhanced leadership capabilities"
                ],
                'long_term': [
                    "Stronger leadership pipeline",
                    "Improved retention of top talent",
                    "Succession planning readiness"
                ]
            },
            'budget_estimation': {
                'per_participant': 150000,  # RUB
                'total_program_cost': high_potential_data['total_high_potential'] * 150000,
                'cost_components': [
                    "External training facilitators",
                    "Materials and resources",
                    "Venue and catering",
                    "Participant time allocation"
                ]
            },
            'success_metrics': [
                "Promotion rates of participants vs non-participants",
                "Retention rates of high-potential employees",
                "360-degree feedback improvement",
                "Business impact of cross-functional projects"
            ]
        }

        return program

    def generate_strategy_report(self):
        """Generate comprehensive HR strategy report"""
        print("=== HR STRATEGY ADVISORY REPORT ===")

        # Turnover Reduction Measures
        turnover_measures = self.suggest_turnover_reduction_measures()
        print(f"\n1. TURNOVER REDUCTION STRATEGY")
        print(f"Problem Departments Identified: {len(turnover_measures)}")

        for dept, measures in list(turnover_measures.items())[:3]:  # Show top 3
            print(f"\n{dept} (Turnover: {measures['current_turnover_rate']}%):")
            print(f"  Immediate Actions:")
            for action in measures['immediate_actions'][:2]:
                print(f"    • {action}")

        # Economic Impact
        economic_effect = self.calculate_economic_effect(10)
        print(f"\n2. ECONOMIC IMPACT ANALYSIS")
        print(f"Current Annual Turnover Cost: {economic_effect['current_annual_turnover_cost']:,} RUB")
        print(f"Potential Savings (10% reduction): {economic_effect['potential_savings_10%_reduction']:,} RUB")
        print(f"Required Investment: {economic_effect['required_investment']:,} RUB")
        print(f"Net Annual Savings: {economic_effect['net_annual_savings']:,} RUB")
        print(f"ROI: {economic_effect['return_on_investment']}%")
        print(f"Payback Period: {economic_effect['payback_period_months']} months")

        # High Potential Program
        high_potential_program = self.develop_high_potential_program()
        print(f"\n3. HIGH POTENTIAL DEVELOPMENT PROGRAM")
        print(f"Program Name: {high_potential_program['program_name']}")
        print(f"Target Audience: {high_potential_program['target_audience']}")
        print(f"Duration: {high_potential_program['program_duration']}")
        print(f"Estimated Budget: {high_potential_program['budget_estimation']['total_program_cost']:,} RUB")

        print(f"\nExpected Outcomes:")
        for outcome in high_potential_program['expected_outcomes']['short_term']:
            print(f"  • {outcome}")

        # Overall Recommendations
        print(f"\n4. OVERALL STRATEGIC RECOMMENDATIONS")
        recommendations = [
            "Implement targeted retention programs in high-turnover departments",
            "Launch leadership development program for high-potential employees",
            "Review and optimize compensation structures",
            "Enhance career progression frameworks",
            "Implement regular employee engagement surveys",
            "Develop departmental succession plans"
        ]

        for i, recommendation in enumerate(recommendations, 1):
            print(f"  {i}. {recommendation}")

        return {
            'turnover_reduction_measures': turnover_measures,
            'economic_impact': economic_effect,
            'high_potential_program': high_potential_program,
            'strategic_recommendations': recommendations
        }