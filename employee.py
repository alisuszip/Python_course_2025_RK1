import pandas as pd
from datetime import datetime
from typing import List, Dict, Any


class Employee:
    """Class representing an employee with all personal, work, and additional information"""

    def __init__(self, employee_data: Dict[str, Any]):
        """
        Initialize Employee object from JSON data

        Args:
            employee_data: Dictionary containing employee information from JSON
        """
        # Employee ID
        self.employee_id = employee_data['employee_id']

        # Personal Information
        personal_info = employee_data['personal_info']
        self.first_name = personal_info['first_name']
        self.last_name = personal_info['last_name']
        self.middle_name = personal_info['middle_name']
        self.full_name = personal_info['full_name']
        self.gender = personal_info['gender']
        self.birth_date = pd.to_datetime(personal_info['birth_date'])
        self.email = personal_info['email']
        self.phone = personal_info['phone']
        self.address = personal_info['address']

        # Work Information
        work_info = employee_data['work_info']
        self.department_id = work_info['department_id']
        self.department_name = work_info['department_name']
        self.position = work_info['position']
        self.salary = work_info['salary']
        self.hire_date = pd.to_datetime(work_info['hire_date'])
        self.experience_years = work_info['experience_years']
        self.performance_score = work_info['performance_score']
        self.skills = work_info['skills']
        self.is_team_lead = work_info['is_team_lead']
        self.work_schedule = work_info['work_schedule']

        # Additional Information
        additional_info = employee_data['additional_info']
        self.education = additional_info['education']
        self.language_skills = additional_info['language_skills']
        self.certifications = additional_info['certifications']
        self.has_company_car = additional_info['has_company_car']
        self.security_clearance = additional_info['security_clearance']

        # Calculated fields
        self._calculate_derived_fields()

    def _calculate_derived_fields(self):
        """Calculate derived fields like age and tenure"""
        # Use generation date from metadata as current date
        self.current_date = pd.to_datetime('2025-10-05')

        # Calculate age
        self.age = (self.current_date - self.birth_date).days / 365.25

        # Calculate tenure
        self.tenure_days = (self.current_date - self.hire_date).days
        self.tenure_years = self.tenure_days / 365.25

        # Age group categorization
        self.age_group = self._get_age_group()

        # Education level numerical mapping
        self.education_level = self._map_education_level()

    def _get_age_group(self) -> str:
        """Categorize employee into age group"""
        if self.age <= 25:
            return "18-25"
        elif self.age <= 35:
            return "26-35"
        elif self.age <= 45:
            return "36-45"
        elif self.age <= 55:
            return "46-55"
        elif self.age <= 65:
            return "56-65"
        else:
            return "65+"

    def _map_education_level(self) -> int:
        """Map education level to numerical value for analysis"""
        education_map = {
            'Среднее специальное': 1,  # Vocational/Technical
            'Высшее': 2,  # Bachelor's
            'Магистратура': 3,  # Master's
            'Кандидат наук': 4,  # PhD Candidate
            'Доктор наук': 5  # Doctor of Sciences
        }
        return education_map.get(self.education, 0)

    def is_high_performer(self, threshold: float = 85.0) -> bool:
        """Check if employee is a high performer"""
        return self.performance_score >= threshold

    def is_short_tenure(self, threshold_years: float = 2.0) -> bool:
        """Check if employee has short tenure (potential turnover risk)"""
        return self.tenure_years < threshold_years

    def has_higher_education(self) -> bool:
        """Check if employee has higher education (Master's, PhD, Doctor)"""
        higher_education = ['Магистратура', 'Кандидат наук', 'Доктор наук']
        return self.education in higher_education

    def get_employee_summary(self) -> Dict[str, Any]:
        """Get comprehensive employee summary for analysis"""
        return {
            # Basic info
            'employee_id': self.employee_id,
            'full_name': self.full_name,
            'gender': self.gender,

            # Demographic info
            'age': round(self.age, 1),
            'age_group': self.age_group,
            'birth_date': self.birth_date,

            # Work info
            'department_id': self.department_id,
            'department_name': self.department_name,
            'position': self.position,
            'salary': self.salary,
            'hire_date': self.hire_date,
            'tenure_years': round(self.tenure_years, 1),
            'experience_years': self.experience_years,
            'performance_score': self.performance_score,
            'is_team_lead': self.is_team_lead,
            'work_schedule': self.work_schedule,
            'skills': self.skills,

            # Education info
            'education': self.education,
            'education_level': self.education_level,
            'language_skills': self.language_skills,
            'certifications': self.certifications,

            # Additional info
            'has_company_car': self.has_company_car,
            'security_clearance': self.security_clearance,

            # Calculated flags
            'is_high_performer': self.is_high_performer(),
            'is_short_tenure': self.is_short_tenure(),
            'has_higher_education': self.has_higher_education()
        }

    def get_analytics_data(self) -> Dict[str, Any]:
        """Get data optimized for analytics (flattened structure)"""
        return {
            'employee_id': self.employee_id,
            'gender': self.gender,
            'age': self.age,
            'age_group': self.age_group,
            'department_name': self.department_name,
            'position': self.position,
            'salary': self.salary,
            'tenure_years': self.tenure_years,
            'performance_score': self.performance_score,
            'is_team_lead': self.is_team_lead,
            'education': self.education,
            'education_level': self.education_level,
            'certifications': self.certifications,
            'skills_count': len(self.skills),
            'languages_count': len(self.language_skills)
        }

    def __str__(self) -> str:
        """String representation of employee"""
        return f"Employee {self.employee_id}: {self.full_name} - {self.position} ({self.department_name})"

    def __repr__(self) -> str:
        """Detailed representation of employee"""
        return (f"Employee(employee_id={self.employee_id}, name='{self.full_name}', "
                f"department='{self.department_name}', position='{self.position}', "
                f"salary={self.salary}, performance={self.performance_score})")

    def to_dict(self) -> Dict[str, Any]:
        """Convert employee to dictionary (reverse of constructor)"""
        return {
            'employee_id': self.employee_id,
            'personal_info': {
                'first_name': self.first_name,
                'last_name': self.last_name,
                'middle_name': self.middle_name,
                'full_name': self.full_name,
                'gender': self.gender,
                'birth_date': self.birth_date.strftime('%Y-%m-%d'),
                'email': self.email,
                'phone': self.phone,
                'address': self.address
            },
            'work_info': {
                'department_id': self.department_id,
                'department_name': self.department_name,
                'position': self.position,
                'salary': self.salary,
                'hire_date': self.hire_date.strftime('%Y-%m-%d'),
                'experience_years': self.experience_years,
                'performance_score': self.performance_score,
                'skills': self.skills,
                'is_team_lead': self.is_team_lead,
                'work_schedule': self.work_schedule
            },
            'additional_info': {
                'education': self.education,
                'language_skills': self.language_skills,
                'certifications': self.certifications,
                'has_company_car': self.has_company_car,
                'security_clearance': self.security_clearance
            }
        }


class EmployeeManager:
    """Manager class for handling multiple employees and bulk operations"""

    def __init__(self, employees: List[Employee] = None):
        self.employees = employees or []

    def add_employee(self, employee: Employee):
        """Add an employee to the manager"""
        self.employees.append(employee)

    def get_employees_by_department(self, department_name: str) -> List[Employee]:
        """Get all employees in a specific department"""
        return [emp for emp in self.employees if emp.department_name == department_name]

    def get_employees_by_position(self, position: str) -> List[Employee]:
        """Get all employees with a specific position"""
        return [emp for emp in self.employees if emp.position == position]

    def get_high_performers(self, threshold: float = 85.0) -> List[Employee]:
        """Get all high-performing employees"""
        return [emp for emp in self.employees if emp.is_high_performer(threshold)]

    def get_team_leads(self) -> List[Employee]:
        """Get all team leads"""
        return [emp for emp in self.employees if emp.is_team_lead]

    def get_employees_with_higher_education(self) -> List[Employee]:
        """Get all employees with higher education"""
        return [emp for emp in self.employees if emp.has_higher_education()]

    def get_analytics_dataframe(self) -> pd.DataFrame:
        """Convert all employees to pandas DataFrame for analysis"""
        data = [emp.get_analytics_data() for emp in self.employees]
        return pd.DataFrame(data)

    def get_summary_statistics(self) -> Dict[str, Any]:
        """Get summary statistics for all employees"""
        if not self.employees:
            return {}

        df = self.get_analytics_dataframe()

        return {
            'total_employees': len(self.employees),
            'gender_distribution': df['gender'].value_counts().to_dict(),
            'average_age': round(df['age'].mean(), 1),
            'average_salary': round(df['salary'].mean(), 2),
            'average_performance': round(df['performance_score'].mean(), 1),
            'average_tenure': round(df['tenure_years'].mean(), 1),
            'team_lead_count': df['is_team_lead'].sum(),
            'department_count': df['department_name'].nunique(),
            'education_distribution': df['education'].value_counts().to_dict()
        }

    def __len__(self) -> int:
        """Return number of employees"""
        return len(self.employees)

    def __getitem__(self, index: int) -> Employee:
        """Get employee by index"""
        return self.employees[index]


# Utility functions for working with employee data
def create_employees_from_json(json_data: List[Dict]) -> List[Employee]:
    """Create list of Employee objects from JSON data"""
    return [Employee(emp_data) for emp_data in json_data]


def load_employees_from_file(file_path: str) -> List[Employee]:
    """Load employees from JSON file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if 'employees' in data:
        return create_employees_from_json(data['employees'])
    else:
        return create_employees_from_json(data)


def export_employees_to_dataframe(employees: List[Employee]) -> pd.DataFrame:
    """Export employees to pandas DataFrame for analysis"""
    data = [emp.get_analytics_data() for emp in employees]
    return pd.DataFrame(data)


if __name__ == "__main__":
    # Example usage
    print("Employee module loaded successfully")
    print("This module provides:")
    print("- Employee class for individual employee data")
    print("- EmployeeManager for bulk operations")
    print("- Utility functions for data loading and analysis")