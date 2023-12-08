from datetime import datetime
from fastapi import Depends, HTTPException, status, APIRouter, Response
from pymongo.collection import ReturnDocument
from employee.schemas.employee_schema import CreateEmployeeSchema, UpdateEmployeeSchema
from core.database import Employee
from authorization.oauth2 import require_user
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
        {'$lookup': {'from': 'employees', 'localField': 'employee',
                     'foreignField': '_id', 'as': 'employee'}},
        {'$unwind': '$employee'},
        {
            '$skip': skip
        }, {
            '$limit': limit
        }
    ]
    employees = employeeListEntity(Employee.aggregate(pipeline))
    return {'status': 'success', 'results': len(employees), 'posts': employees}

# [...] Create Employee
@router.post('/', status_code=status.HTTP_201_CREATED)
def create_employee(employee: CreateEmployeeSchema, username: str = Depends(require_user)):
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
        new_post = employeeListEntity(Employee.aggregate(pipeline))[0]
        return new_post
    except DuplicateKeyError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Employee with email: '{employee.email}' already exists")

# [...] Update Post
@router.put('/{id}')
def update_employee(id: str, payload: UpdateEmployeeSchema, emp_id: str = Depends(require_user)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid id: {id}")
    updated_employee = Employee.find_one_and_update(
        {'_id': ObjectId(id)}, {'$set': payload.dict(exclude_none=True)}, return_document=ReturnDocument.AFTER)
    if not updated_employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No post with this id: {id} found')
    return employeeEntity(updated_employee)

# [...] Get Single Post
@router.get('/{id}')
def get_employee(id: str, emp_id: str = Depends(require_user)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid id: {id}")
    pipeline = [
        {'$match': {'_id': ObjectId(id)}},
        {'$lookup': {'from': 'employees', 'localField': 'employee',
                     'foreignField': '_id', 'as': 'employee'}},
        {'$unwind': '$employee'},
    ]
    db_cursor = Employee.aggregate(pipeline)
    results = list(db_cursor)

    if len(results) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No post with this id: {id} found")

    post = employeeListEntity(results)[0]
    return post
