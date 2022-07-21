
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy.orm import Session
import models
from models import Employee, Department, Application, Position
from database import sessionLocal, engine
from validators import EmployeeResponse, EmployeeRequest, DepartmentResponse, DepartmentRequest, ApplicationResponse, ApplicationRequest, PositionResponse, PositionRequest, PositionResponse

app=FastAPI(debug=True)

async def get_db():
	db = sessionLocal()
	try:
		yield db 
	finally:
		db.close()

@app.on_event("startup")
async def on_startup():
    models.Base.metadata.create_all(bind=engine)

@app.get('/')
async def trial_api():
    return "hello-world"

#_____________employee apis _______________#


@app.get(
    "/employee/",
    response_model = List[EmployeeResponse],
    tags = ["Employee"],
    )
async def read(db : Session = Depends(get_db)):

	result = db.query(Employee).all()
	if not result:
		raise HTTPException(
			status_code = 404,
			detail = "details not found",
			)
	return result



@app.post(
    "/employee/",
    response_model = EmployeeResponse,
    tags = ["Employee"],
    )
async def create(
	employee : EmployeeRequest,
	db : Session = Depends(get_db),
):  
    obj = db.query(Employee).where(Employee.personal_email_id == employee.personal_email_id).first()
    obj2 = db.query(Employee).where(Employee.company_email_id == employee.company_email_id).first()
    employee.leave_balance = 2
    employee.wfh_balance =2
    if obj:
        raise HTTPException( status_code = 409,
        detail = "{} email already exists. please try using another email.".format(employee.personal_email_id))
    elif obj2:
        raise HTTPException(status_code = 409,
        detail = "{} email alrady exists. Please enter correct email.".format(employee.company_email_id))
    employee_dict = employee.dict()
    emp = Employee(**employee_dict)
    db.add(emp)
    db.commit()
    db.refresh(emp)
    return emp


@app.get(
    "/employee/{employee_id}/",
    response_model = EmployeeResponse,
    tags = ["Employee"],)
async def get_by_id(
	employee_id = str,
	db : Session = Depends(get_db)
):

    result = db.query(Employee).where(Employee.id == employee_id).first()
    if not result:
        raise HTTPException(
        status_code = 404,
        detail = "employee with id {} does not exist".format(employee_id),
        )
    return result


@app.patch(
    "/employee/{employee_id}/",
    response_model = EmployeeResponse,
    tags = ["Employee"],
    )
async def update(
	employee_id : str,
	employee : EmployeeRequest,
	db : Session = Depends(get_db)
):
    obj = db.query( Employee ).where( Employee.id == employee_id).first()
    email = db.query(Employee).where( Employee.personal_email_id == employee.personal_email_id).first()
    email2 = db.query(Employee).where( Employee.company_email_id == employee.company_email_id).first()
    if not obj:
        raise HTTPException( 
            status_code = 404, 
            detail = "employee with id {} not found".format(employee_id)
            )
    if email:
        raise HTTPException( status_code = 409,
        detail = "{} email already exists. Please try again with another email.".format(employee.personal_email_id))
    elif email2:
        raise HTTPException( status_code = 409,
        detail = "company email {} already exists. Please enter correct company email.".format(employee.company_email_id))
    employee_dict = employee.dict(exclude_unset = True)
    for key,values in employee_dict.items():
        setattr(obj, key, values)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj
    

@app.delete("/employee/{employee_id}",tags = ["Employee"]) 
async def delete(
	employee_id : str,
	db : Session = Depends(get_db),
):
    obj = db.query(Employee).where(Employee.id == employee_id).first()
    if not obj:
        raise HTTPException( status_code = 404, detail = "Employee with id {} does not exist".format(employee_id))
    db. delete(obj)
    db.commit()
    return {"ok": "True"}




#_______________department apis ___________________#



@app.get("/department/", 
    response_model = List[DepartmentResponse], 
    tags = ["Department"])
async def read_all( db : Session = Depends(get_db)
):
    obj = db.query(Department).all()
    return obj


@app.get("/department/{department_id}", 
    response_model = DepartmentResponse,
    tags = ["Department"])
async def get_by_id(
	department_id : str,
	db : Session = Depends(get_db),
):
    obj = db.query(Department).where(Department.id == department_id).first()
    if not obj:
        raise HTTPException(status_code = 404, detail = "Department with id {} does not exist ".format(department_id))
    return obj


@app.post("/department/",
    response_model = DepartmentResponse,
    tags = ["Department"])
async def create(
	department : DepartmentRequest,
	db : Session = Depends(get_db)
):
    dep_dict = department.dict()
    obj = db.query(Department).where(Department.department == department.department).first()
    if obj:
        raise HTTPException(statu_code =409,
        detail = "Department already exists")
    dep = Department(**dep_dict)
    db.add(dep)
    db.commit()
    db.refresh(dep)
    return dep


@app.patch("/department/{id}",
    response_model = DepartmentResponse,
    tags = ['Department'])
async def update( id : str, 
    department : DepartmentRequest,
    db : Session = Depends(get_db),
):
    obj = db.query(Department).where(Department.id == id).first()
    if not obj:
        raise HTTPException(status_code = 404, detail = "Department with id {} does not exist".format(id))
    
    obj2 = db.query(Department).where(Department.department == department.department).first()
    if obj2:
        raise HTTPException( status_code = 409,
        detail = "Department already exists")

    dep_dict = department.dict(exclude_unset = True)
    for key, values in dep_dict.items():
        setattr(obj,key,values)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@app.delete("/department/{department}",
    response_model = DepartmentResponse,
    tags = ["Department"])
async def delete( 
    id : str, 
    db : Session = Depends(get_db),
):

   obj = db.query(Department).where(Department.id == id).first()
   if not obj:
       raise HTTPException(status_code = 404, detail = "Department with id {} does not exist".format(id))

   db.delete(obj)
   db.commit()
   db.refresh(obj)
   return {"ok": "True"}



#===============application apis =========================#




@app.get("/application/",
    response_model = List[ApplicationResponse],
    tags = ["Application"])
async def read_all(db : Session = Depends(get_db)):
    obj = db.query(Application).all()
    if not obj:
        raise HTTPException( status_code = 404,
        detail = "Details not found")
    return obj


@app.get("/application/{application_id}",
    response_model = ApplicationResponse,
    tags = ["Application"])
async def read_by_id( application_id : str, 
    db : Session = Depends(get_db)
    ):
    obj = db.query(Application).where(Application.id == application_id).first()
    if not obj:
        raise HTTPException(status_code = 404, detail = "details not found for id {}".format(application_id))
    return obj



@app.post("/application/",
    response_model = ApplicationResponse,
    tags = ['Application'])
async def create( application : ApplicationRequest, 
    db : Session = Depends(get_db)
    ):
    obj_dict = application.dict()
    app = Application(**obj_dict)
    db.add(app)
    db.commit()
    db.refresh(app)
    return app




@app.patch("/application/{application_id}",
    response_model = ApplicationResponse,
    tags = ["Application"])
async def update( id : str, application : ApplicationRequest, 
    db : Session = Depends(get_db)
):
    obj = db.query(Application).where(Application.id == id).first()
    if not obj:
        raise HTTPException(status_code = 404, detail = "details not found for id {}".format(id))
    current_dict = application.dict(exclude_unset = True)
    for key, values in current_dict.items():
        setattr(obj, key, values)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


 
@app.delete("/application/{application_id}",
    response_model = ApplicationResponse,
    tags = ["Application"])
async def delete(id : str, 
    db : Session = Depends(get_db),
    ):
    obj = db.query(Application).where(Application.id == id).first()
    if not obj:
        raise HTTPException(status_code = 404, detail = "Details not found for id {}".format(id))
    db.delete(obj)
    db.commit()
    db.close()
    return "Success"


#================position api=====================#


@app.get("/position/",
    response_model = List[PositionResponse],
    tags = ['Position'])
async def read_all( db: Session = Depends(get_db)):
    obj = db.query(Position).all()
    if not obj:
        raise HTTPException(status_code = 404,
        detail = "Details not found")
    return obj


@app.get("/position/{Position_id}",
    response_model = PositionResponse,
    tags = ['Position'])
async def read_by_id( position_id : str, 
    db : Session = Depends(get_db),
    ):
    obj = db.query(Position).where(Position.id == position_id).first()
    if not obj:
        raise HTTPException(status_code = 404, detail = 'Details not found for id {}'.format(position_id))
    return obj


@app.post("/position/",
    response_model = PositionResponse,
    tags = ['Position'])
async def create( position : PositionRequest , 
    db : Session = Depends(get_db)
    ):
    obj_dict = position.dict()
    obj2 =db. query(Position).where(Position.position == position.position).first()
    if obj2:
        raise HTTPException( status_code = 409,
        detail = "Position {} already exists".format(position.position))
    obj = Position(**obj_dict)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    print(obj)
    return obj


@app.patch("/position/{position_id}",
    response_model = PositionResponse,
    tags = ['Position'])
async def update(position_id : str,
    position : PositionRequest,
    db : Session = Depends(get_db),
):
    obj = db.query(Position).where(Position.id == position_id).first()
    if not obj:
        raise HTTPException(status_code = 404, detail = "Details not found for id {}".format(position_id))
    
    obj2 = db.query(Position).where(Position.position == position.position).first()
    if obj2:
        raise HTTPException( status_code = 422,
        detail = "Position {} already exists".format(position.position))

    current_dict = position.dict(exclude_unset = True)
    for key,values in current_dict.items():
        setattr(obj, key, values)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@app.delete(
    "/position/{position_id}",
    response_model = PositionResponse,
    tags = ['Position']
)
async def delete(
    position_id : str,
    db : Session = Depends(get_db),
):
    obj = db.query(Position).where(Position.id == position_id).first()
    if not obj:
        raise HTTPException( status_code = 404, detail = "Details not found for id {}".format(position_id))
    db.delete(obj)
    db.commit()
    db.close()

    return {"msg":"success"}







