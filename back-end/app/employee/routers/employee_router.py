from datetime import datetime
from fastapi import Depends, HTTPException, status, APIRouter, Response
from pymongo.collection import ReturnDocument
from app.employee.schemas.employee_schema import (EmployeeBaseSchema,
                                                  CreateRegularEmployeeSchema,
                                                  CreateContractualEmployeeSchema,
                                                  UpdateRegularEmployeeSchema,
                                                  UpdateContractualEmployeeSchema)
from app.core.database import Employee
from app.core.oauth import require_user
from app.employee.serializers.employee_serializers import employeeEntity, employeeListEntity
from bson.objectid import ObjectId
from pymongo.errors import DuplicateKeyError

# [...] imports

router = APIRouter()

# [...] Get All Employees
@router.get('/')
def get_employees(limit: int = 10, page: int = 1, search: str = '', username: str = Depends(require_user)):
    skip = (page - 1) * limit

    pipeline = [
        {'$match': {}},
        {
            '$skip': skip
        }, {
            '$limit': limit
        }
    ]

    employees = employeeListEntity(Employee.aggregate(pipeline))
    return {'status': 'success', 'results': len(employees), 'employees': employees}

# [...] Create Employee
@router.post('/', status_code=status.HTTP_201_CREATED)
def create_employee(employee: EmployeeBaseSchema, username: str = Depends(require_user)):
    employee.created_at = datetime.utcnow()
    employee.updated_at = employee.created_at

    try:
        result = Employee.insert_one(employee.dict())
        pipeline = [
            {'$match': {'_id': result.inserted_id}},
            {'$lookup': {'from': 'employees', 'localField': 'employee',
                        'foreignField': '_id', 'as': 'employee'}},
            {'$unwind': '$user'},
        ]
        new_employee = employeeListEntity(Employee.aggregate(pipeline))[0]
        return new_employee
    except DuplicateKeyError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Employee with email: '{employee.email}' already exists")

# [...] Create regular Employee
@router.post('/regular', status_code=status.HTTP_201_CREATED)
def create_regular_employee(regular_employee: CreateRegularEmployeeSchema, username: str = Depends(require_user)):
    regular_employee.created_at = datetime.utcnow()
    regular_employee.updated_at = regular_employee.created_at

    try:
        result = Employee.insert_one(regular_employee.dict())
        return employeeEntity(Employee.find_one({'_id': result.inserted_id}))
    except DuplicateKeyError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Employee with email: '{regular_employee.email}' already exists")

# [...] Create Contractual Employee
@router.post('/contractual', status_code=status.HTTP_201_CREATED)
def create_contractual_employee(contractual_employee: CreateContractualEmployeeSchema, username: str = Depends(require_user)):
    contractual_employee.created_at = datetime.utcnow()
    contractual_employee.updated_at = contractual_employee.created_at

    try:
        result = Employee.insert_one(contractual_employee.dict())
        return employeeEntity(Employee.find_one({'_id': result.inserted_id}))
        # pipeline = [
        #     {'$match': {'_id': result.inserted_id}},
        #     {'$lookup': {'from': 'employees', 'localField': 'employee',
        #                 'foreignField': '_id', 'as': 'employee'}},
        #     {'$unwind': '$user'},
        # ]
        # new_employee = employeeListEntity(Employee.aggregate(pipeline))[0]
        # return new_employee
    except DuplicateKeyError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Employee with email: '{contractual_employee.email}' already exists")

# [...] Update Regular Employee
@router.put('/regular/{id}')
def update_regular_employee(id: str, payload: UpdateRegularEmployeeSchema, username: str = Depends(require_user)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid id: {id}")

    updated_employee = Employee.find_one_and_update(
        {'_id': ObjectId(id)}, {'$set': payload.dict(exclude_none=True)}, return_document=ReturnDocument.AFTER)

    if not updated_employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No employee with this id: {id} found')
    return employeeEntity(updated_employee)

# [...] Update Contractual Employee
@router.put('/contractual/{id}')
def update_contractual_employee(id: str, payload: UpdateContractualEmployeeSchema, username: str = Depends(require_user)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid id: {id}")

    updated_employee = Employee.find_one_and_update(
        {'_id': ObjectId(id)}, {'$set': payload.dict(exclude_none=True)}, return_document=ReturnDocument.AFTER)

    if not updated_employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No employee with this id: {id} found')
    return employeeEntity(updated_employee)

# [...] Get Single Employee
@router.get('/{id}')
def get_employee(id: str, username: str = Depends(require_user)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid id: {id}")

    employee = Employee.find_one({'_id': ObjectId(id)})

    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No employee with this id: {id} found')

    return employeeEntity(employee)

# [...] Delete Employee
@router.delete('/{id}')
def delete_employee(id: str, username: str = Depends(require_user)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid id: {id}")

    result = Employee.find_one_and_delete({'_id': ObjectId(id)})

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No employee with this id: {id} found')
    return Response(status_code=status.HTTP_204_NO_CONTENT)
