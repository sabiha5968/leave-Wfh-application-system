
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import session
from typing import List
from sqlalchemy.orm import Session

from database import sessionLocal

app=FastAPI(debug=True)


def get_db():
	db = sessionLocal()
	try:
		yield db 
	finally:
		db.close()

#_____________employee apis _______________#


#@app.get("/empployee/", response_model = List[EmployeeResponse])
#async def read(db : session = Depends(get_db)):
#
#	result = db.query(employee).all()
#	if not result:
#		raise HTTPException(
#			status_code = 404,
#			detail = "details not found",
#			)
#	return result
#
#
#
#@app.post("/employee/",response_model = EmployeeResponse)
#async def create(
#	employee : EmployeeReques,
#	db : session = Depends(get_dba),
#):
#
#
#    employee_dict = employee.dict()
#    result = db.query(employee).where(employee.email_id == employee_dict["email_id"])
#    if result:
#    	raise HTTPException(
#    		sttaus_code = 422,
#    		detail = "email already exists",
#    )
#
#
#    	emp = employee(**employee_dict)
#    	db.add(emp)
#    	db.commit(emp)
#    	db.refresh(emp)
#    	print(emp)
#
#    	return employee
#
#
#
@app.get("/employee/{id}/",response_model = EmployeeResponse)
async def get_by_id(
	id = str,
	db : session = Depends(get_db)
):

     result = db.query(employee).where(employee.id == id).first()
     if not result:
     	raise HTTPException(
     		status_code = 404,
     		detail = "detail not found",
     		)
     return result





@app.path("/employee/{id}/",response_model = Employeeresponse)
async def update(
	id : str,
	employee : EmployeeRequest,
	db : Session = Depends(get_db)
):
 result = db.query( employee ).where( employee.id == id).first()



@app.delete("/employee/{id}") 
async def delete(
	id : str,
	db : Session = Depends(get_db),
):
    obj = db.query(employee).where(employee.id == id).first()
    if not obj:
    	raise HTTPException( status_code = 404, detail = "data not found")
    db. delete(obj)
    db.commit()
    return {"ok" : "True"}




#_______________department apis ___________________#



@app.get("/department/", response_model = List[DepartmentResponse])
async def read_all( db : Session = Depends(get_db)
):
     obj = db.query(department).all()
     return obj




@app.get("/department/{id}", response_model = DepartmentResponse)
async def get_by_id(
	id : str,
	db : Session = Depends(get_db),
):
    obj = db.query(department).where(department.id == id).first()
    if not obj:
    	raise HTTPException(status_code = 404, detail = "data not found")
    return obj




@app.post("/department/",response_model = DepartmentResponse)
async def create(
	department : DepartmentRequest,
	db : Session = Depends(get_db)
):
    dep_dict = department.dict()
    result = db.query(department).where(department.name == department_dict["name"]).first()
    if result:
    	raise HTTPException(status_code = 422, detail = "department already exists")
    dep = department(**department_dict)
    db.add(dep)
    db.commit()
    db.refresh(dep)
    return dep



@app.patch("/department/{id}",response_model = DepartmentResponse)
async def update( id : str, department : DepartmentRequest, db : Session = Depends(get_db),
):
    obj = db.query(department).where(department.id == id).first()
    if not obj:
    	raise HTTPException(status_code = 404, detail = "data not found")

    dep_dict = department.dict(exclude_unset = True)
    for key, value in dep_dict.items():
    	setattr(obj,key,values)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj



@app.delete("/department/{id}",response_model = DepartmentResponse)
async def delete(id : str, department : DepartmentRequest, db : Session = Depends(get_db),
):

   obj = db.query(department).where(department.id ==id).first()
   if not obj:
       raise HTTPException(status_code = 404, details = "data not found")
   dep_dict = department.dict(exclude_unset = True)
   for key, value in dep_dict.items():
       setattr(obj,key, values)
   db.add(obj)
   db.commit()
   db.refresh(obj)
   return obj



#===============application apis =========================#




@app.get("/application/",response_model = List[ApplicationResponse])
async def read_all(db : Session = Depends(get_db)):
    obj = db.query(application).all()
    if not obj:
        raise HTTPException(status_code = 404, details = "data not found")
    return obj






@app.get("/application/{id}",response_model = ApplicationResponse)
async def read_by_id( id : str, db : Session = Depends(get_db),):
    obj = db.query(application).where(application.id ==id).first()
    if not obj:
        raise HTTPException(status_code = 404, details = "details not found",)
    return obj



@app.post("/application/",response_model = ApplicationResponse)
async def create( application : Applicationrequest, db : Session = Depends(get_db)):
    obj_dict = application.dict()
    app = application(**obj_dict)
    db.add(app)
    db.commit()
    db.refresh(app)
    return app




@app.patch("/application/{id}",response_model = ApplicationResponse)
async def update( id : str, app : ApplicationRequest, db : Session = Depends(get_db),):
    obj = db.query(application).where(applicatio_id == id).frist()
    if not obj:
        raise HTTPException(status_code = 404, details = "details not found")
    current_dict = applciation.dict(exclude_unset = True)
    for key, values in current_dict.items():
        setattr(obj, keys, values)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


 
@app.delete("/application/{id}",response_model = ApplicationReponse)
async def delete(email_id : str, db : Session = Depends(get_db),):
    obj = db.query(application).where(application_email_id == email_id).first()
    if not obj:
        raise HTTPException(status_code = 404, details = "Details not found")
    db.delete(obj)
    db.commit()
    db.close()
    return "Success"




#================position api=====================#



@app.get("/position/",response_model = List[positionResponse])
async def read_all( db: Session = Depends(get_db)):
    obj = db.query(application).all()
    return obj



@app.get("/application/{id}",response_model = PositionResponse)
async def read_by_id( id : str, db : Session = Depends(get_db)):
    obj = db.query(position).where(position_id == id).first()
    if not obj:
        raise HTTPExcception(status_code = 404, details = 'details not found')
    return obj



@app.post("/position/",response_model = positionResponse)
async def create( position : PositionRequest, db : Session = Depends(get_db)):
    obj_dict = position.dict()
    obj = position(**obj_dict)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@app.patch("/position/{id}",response_model = PositionResponse)
async def update(position : Positionrequest):
    obj = db.query(position).where(position_id == id).first()
    if not obj:
        raise HTTPException(status_code = 404, details = "details not found")
    return obj


@app.delete("/position/{id}",response_tabe = PostionResponse)
async def delete(db : Session = Depends(get_db)):
    obj = db.query(position).where(position_id == id).first()
    if not obj:
        raise HTTPException( status_code = 404, details = "details not found")
    db.delete(obj)
    db.commit()
    db.close()
    return "Success"







