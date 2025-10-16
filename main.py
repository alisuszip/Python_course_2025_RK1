import json
from employee import Employee
from analyzers import DemographicAnalyzer
from analyzers import TurnoverAnalyzer
from analyzers import EducationAnalyzer
from analyzers import CareerDevelompentAnalyzer
from analyzers import HRStrategyAdvisor


def load_data(json_file_path: str):
    """Load data from JSON file"""
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    employees = []
    for emp_data in data['employees']:
        employees.append(Employee(emp_data))

    return employees


def main():
    """Main function to run all analyses"""
    print("Loading company data...")
    employees = load_data('company.json')
    print(f"Loaded {len(employees)} employees\n")

    # Initialize all analyzers
    demographic_analyzer = DemographicAnalyzer.DemographicAnalyzer(employees)
    turnover_analyzer = TurnoverAnalyzer.TurnoverAnalyzer(employees)
    education_analyzer = EducationAnalyzer.EducationAnalyzer(employees)
    career_analyzer = CareerDevelompentAnalyzer.CareerDevelopmentAnalyzer(employees)
    strategy_advisor = HRStrategyAdvisor.HRStrategyAdvisor(employees)

    # Run all analyses
    print("=" * 60)
    demographic_report = demographic_analyzer.generate_demographic_report()

    print("\n" + "=" * 60)
    turnover_report = turnover_analyzer.generate_turnover_report()

    print("\n" + "=" * 60)
    education_report = education_analyzer.generate_education_report()

    print("\n" + "=" * 60)
    career_report = career_analyzer.generate_career_development_report()

    print("\n" + "=" * 60)
    strategy_report = strategy_advisor.generate_strategy_report()

    print("\n" + "=" * 60)
    print("ALL ANALYSES COMPLETED SUCCESSFULLY!")


if __name__ == "__main__":
    main()