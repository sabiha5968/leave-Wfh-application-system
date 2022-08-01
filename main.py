

from fastapi import FastAPI, HTTPException, Depends,Request, Form
from sqlalchemy.orm import Session
from typing import List
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
import models
from models import Employee, Department, Application, Position
from database import sessionLocal, engine
from validators import EmployeeResponse, EmployeeRequest, DepartmentResponse, DepartmentRequest, ApplicationResponse, ApplicationRequest, PositionResponse, PositionRequest, PositionResponse

app=FastAPI(debug=True)


templates = Jinja2Templates(directory = "template")





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



@app.post("/applications/",response_class = HTMLResponse)
async def read_form(request : Request,db : Session = Depends(get_db)):
    return templates.TemplateResponse("application_form.html",{"request":request})

@app.post("/add_employee/",response_class = HTMLResponse)
async def read_emp_form(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("add_employee.html",{"request":request})

@app.post("/view_employee_list/", response_class = HTMLResponse)
async def read_employee_list(request : Request,db :Session = Depends(get_db)):
    return templates.TemplateResponse("employee_list.html",{"request":request})

@app.post("/view_application_list/",response_class = HTMLResponse)
async def read_application_list(request : Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("dashboard.html",{"request": request})

@app.post("/add_department/",response_class = HTMLResponse)
async def add_department(request : Request, db : Session = Depends(get_db)):
    return templates.TemplateResponse("add_department.html",{"request":request})

@app.post("/add_position/",response_class = HTMLResponse)
async def add_position(request:Request):
    return templates.TemplateResponse("add_position.html",{"request" : request})

#_____________employee apis _______________#


@app.get(
    "/employee/",
    response_model = EmployeeResponse,
    response_class = HTMLResponse,
    tags = ["Employee"],
    )
async def read(request: Request,db : Session = Depends(get_db)):
    
    select_query = db.query(Employee.id,Employee.first_name,Employee.last_name,Employee.company_email_id,Employee.reporting_manager, Department.department, Position.position)
    join_query = select_query.outerjoin(Department).outerjoin(Position)
    result = join_query.all()
    return templates.TemplateResponse("employee_list.html",{"request":request,"result":result})

    # for i in result:
    #     print(i.Position.position)
    #     print(i.Department.department)


	# if not result:
	# 	raise HTTPException(
	# 		status_code = 404,
	# 		detail = "details not found",
	# 		)
	# return templates.TemplateResponse("employee_list.html",
    # {"request" : request, "result" : result}
    #  )



@app.post(
    "/employee/",
    response_model = EmployeeResponse,
    response_class = HTMLResponse,
    tags = ["Employee"],
    )
async def create(
    request : Request,
	employee : EmployeeRequest,
	db : Session = Depends(get_db),
):  
    employee.wfh_balance =2
    employee.leave_balance = 2
    obj = db.query(Employee).where(Employee.personal_email_id == employee.personal_email_id).first()
    if obj:
        raise HTTPException( status_code = 409,
        detail = "{} email already exists. please try using another email.".format(employee.personal_email_id))
    obj2 = db.query(Employee).where(Employee.company_email_id == employee.company_email_id).first()
    if obj2:
        raise HTTPException(status_code = 409,
        detail = "{} email alrady exists. Please enter correct email.".format(employee.company_email_id))
    employee_dict = employee.dict()
    emp = Employee(**employee_dict)
    db.add(emp)
    db.commit()
    db.refresh(emp)
    return templates.TemplateResponse("employee_list.html",{"request":request, "results" :emp})


@app.get(
    "/employee/{employee_id}/",
    response_model = EmployeeResponse,
    response_class = HTMLResponse,
    tags = ["Employee"],)
async def get_by_id(
    request  : Request,
	employee_id : str,
	db : Session = Depends(get_db)
):
    result = db.query(Employee,Position,Department)
    join_query= result.outerjoin(Position).outerjoin(Department)
    results =join_query.where(Employee.id == employee_id).first()
    print(results.Position.position)
    return templates.TemplateResponse("emp_details.html",{"request":request,"result":results})
    print(select_query)
    

    # r2 = r1.query(Employee).where(Employee.id == employee_id).first()
    # result= r1.query(Employee,).where(Employee.id == employee_id).first()
    # print(result.__dict__)

    #  if not result:
    #     raise HTTPException(
    #     status_code = 404,
    #     detail = "employee with id {} does not exist".format(employee_id),
    #     )
    # print(result)
    # return templates.TemplateResponse("emp_details.html",{"request" : request, "results":result})


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
    return {"msg" : "Success"}




#_______________department apis ___________________#



@app.get(
    "/department/", 
    response_model = DepartmentResponse, 
    response_class = HTMLResponse,
    tags = ["Department"])
async def read_all( request: Request,db : Session = Depends(get_db)
):
    obj = db.query(Department).all()
    if not obj:
        raise HTTPException(
            status_code = 404,
            detail = "details not found",
        )
    return templates.TemplateResponse("department_details.html",{"request" : request, "results":obj})


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


@app.post("/departments/",
    response_model = DepartmentResponse,
    response_class =HTMLResponse,
    tags = ["Department"])
async def create(
    request:Request,
	department : DepartmentRequest,
	db : Session = Depends(get_db)
):
    dep_dict = department.dict()
    obj = db.query(Department).where(Department.department == department.department).first()
    # if obj:
    #     raise HTTPException(statu_code =409,
    #     detail = "Department already exists")
    dep = Department(**dep_dict)
    db.add(dep)
    db.commit()
    db.refresh(dep)
    return templates.TemplateResponse("department_details.html",{"request":request})


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
   return {"msg" : "Success"}


@app.get("/home/",response_class = HTMLResponse)
async def read_notes(request:Request,db :Session =Depends(get_db)):
    return templates.TemplateResponse("Home2.html",{"request":request})



#===============application apis =========================#


@app.get("/application/",
    response_model = ApplicationResponse,
    response_class = HTMLResponse,
    tags = ["Application"])
async def read_all(request: Request,db : Session = Depends(get_db)):
    select_query = db.query(Application.application_type,Application.subject,Employee.id, Employee.first_name,Employee.last_name)
    join_query = select_query.outerjoin(Employee)
    obj = join_query.all()
    for i in obj:
        print(i.application_type)
        print(i.subject)
    return templates.TemplateResponse("dashboard.html",{"request":request, "obj":obj})
  
    # if not obj:
    #     raise HTTPException( 
    #         status_code = 404,
    #     detail = "Details not found",
    #     )


@app.get("/application/{application_id}",
    response_model = ApplicationResponse,
    response_class = HTMLResponse,
    tags = ["Application"])
async def read_by_id( 
    request : Request,
    application_id : str, 
    db : Session = Depends(get_db)
):
    obj = db.query(Application).where(Application.id == application_id).first()
    print(obj)
    if not obj:
        raise HTTPException(status_code = 404, detail = "details not found for id {}".format(application_id))
    return templates.TemplateResponse("application_by_id.html",{"request":request,"obj":obj})



@app.post("/application1/",
    response_model = ApplicationResponse,
    response_class = HTMLResponse,
    tags = ['Application'])
async def create( request:Request, application : ApplicationRequest, 
    db : Session = Depends(get_db)
    ):
    obj_dict = application.dict()
    app = Application(**obj_dict)
    db.add(app)
    db.commit()
    db.refresh(app)
    return templates.TemplateResponse("dashboard.html",{"request":request})




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
    return {"msg" : "Success"}


#================position api=====================#


@app.get(
    "/position/",
    response_model = PositionResponse,
    response_class = HTMLResponse,
    tags = ['Position']
)
async def read_all( 
    request: Request,
    db: Session = Depends(get_db),
):
    obj = db.query(Position).all()
    if not obj:
        raise HTTPException(
            status_code = 404,
        detail = "Details not found")
    return templates.TemplateResponse(
        "position_details.html",
        {
            "request":request,
            "results":obj,        
        }
    )


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
    response_class = HTMLResponse,
    tags = ['Position']
)
async def create( 
    request : Request, 
    position : PositionRequest, 
    # = Form(...), 
    db : Session = Depends(get_db),
):
   
    obj_dict = position.dict()
    obj2 =db. query(Position).where(Position.position == position.position).first()
    # if obj2:
    #     raise HTTPException( status_code = 409,
    #     detail = "Position {} already exists".format(position.position))
    obj = Position(**obj_dict)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    print(obj.__dict__)
    # return templates.TemplateResponse("add_position.html",{"request":request})
    return templates.TemplateResponse(
        "Home2.html",
        {
            "request":request,
            "results":obj,        
        }
    )


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
    response_class = HTMLResponse,
    response_model = PositionResponse,
    tags = ['Position']
)
async def delete(
    request : Request,
    position_id : str,
    db : Session = Depends(get_db),
):
    obj = db.query(Position).where(Position.id == position_id).first()
    if not obj:
        raise HTTPException( status_code = 404, detail = "Details not found for id {}".format(position_id))
    db.delete(obj)
    db.commit()
    db.close()

    return templates.TemplateResponse("position_details.html",{"request": request})







