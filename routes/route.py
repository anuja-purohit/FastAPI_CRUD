from fastapi import APIRouter,HTTPException,Query,Path
from fastapi.responses import JSONResponse
from config.database import db
from models.todos import Todo
from models.students import Student,StudentUpdate
from config.database import collection_name
from schema.schemas import list_serial, individual_serial
from bson import ObjectId 

router = APIRouter()

#Get Request Method
@router.get("/")
async def get_root():
    todos ="Api working"
    return todos

@router.post("/students", status_code=201)
async def create_student(student: Student):
    inserted_student = collection_name.insert_one(student.dict())
    return {"id": str(inserted_student.inserted_id)}

@router.get("/students", response_model=dict)
async def list_students(country: str = Query(None, description="To apply filter of country"),
                        age: int = Query(None, description="Only records which have age greater than equal to the provided age should be present in the result")):
    """
    List students with optional filters.
    """
    query = {}
    if country:
        query['address.country'] = country
    if age:
        query['age'] = {'$gte': age}
    
    students = db.Library_collection.find(query)
    student_list = [{"name": student["name"], "age": student["age"]} for student in students]
    return {"data": student_list}


@router.get("/students/{id}", response_model=Student)
async def get_student(id: str = Path(..., title="The ID of the student")):
    """
    Fetch details of a specific student by ID.
    """
    student = db.Library_collection.find_one({"_id": ObjectId(id)})
    if student:
        return student
    else:
        raise HTTPException(status_code=404, detail="Student not found")
    
@router.patch("/students/{id}", status_code=204)
async def update_student(id: str, student_update: StudentUpdate):
    """
    Update details of a specific student by ID.
    """
    # Convert the Pydantic model to a dictionary
    update_data = student_update.dict(exclude_unset=True)
    
    # Update the student in the database
    result = db.Library_collection.update_one({"_id": ObjectId(id)}, {"$set": update_data})
    
    # Check if the student was found and updated
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    return JSONResponse(content={})



@router.delete("/students/{id}", status_code=200)
async def delete_student(id: str = Path(..., title="The ID of the student")):
    """
    Delete a specific student by ID.
    """
    # Delete the student from the database
    result = db.Library_collection.delete_one({"_id": ObjectId(id)})
    
    # Check if the student was found and deleted
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    else:
        return {"message": "Student deleted successfully"}