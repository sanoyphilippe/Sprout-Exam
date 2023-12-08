def employeeEntity(employee) -> dict:
    return {
        "id": str(employee["_id"]),
        "first_name": employee["first_name"],
        "last_name": employee["last_name"],
        "email": employee["email"],
        "emp_type": employee["emp_type"],
        "number_of_leaves": employee["number_of_leaves"],
        "benefits": employee["benefits"],
        "contract_end_date": employee["contract_end_date"],
        "project": employee["project"],
        "created_at": employee["created_at"],
        "updated_at": employee["updated_at"]
    }

def employeeResponseEntity(employee) -> dict:
    return {
        "id": str(employee["_id"]),
        "first_name": employee["first_name"],
        "last_name": employee["last_name"],
        "email": employee["email"],
        "emp_type": employee["emp_type"],
        "number_of_leaves": employee["number_of_leaves"],
        "benefits": employee["benefits"],
        "contract_end_date": employee["contract_end_date"],
        "project": employee["project"],
        "created_at": employee["created_at"],
        "updated_at": employee["updated_at"]
    }

def embeddedEmployeeResponse(employee) -> dict:
    return {
        "id": str(employee["_id"]),
        "first_name": employee["first_name"],
        "last_name": employee["last_name"],
        "email": employee["email"],
        "emp_type": employee["emp_type"]
    }

def employeeListEntity(employees) -> list:
    return [employeeEntity(employee) for employee in employees]

