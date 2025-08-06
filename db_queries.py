from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from sqlalchemy import and_
from typing import List, Optional

from models import Student, Enrollment, Course, EnrollmentStatusEnum

# Fast query for students in a course with optional status
async def get_students_in_course(session, course_id: int, status: Optional[str]=None) -> List[Student]:
    
    stmt = select(Student).join(Enrollment).where(
        and_(
            Enrollment.course_id == course_id,
            Enrollment.student_id == Student.id
        )
    )
    if status:
        stmt = stmt.where(Enrollment.status == status)
    stmt = stmt.options(joinedload(Student.enrollments))

    # Optionally, load only required columns or use only() for memory efficiency in very large datasets
    result = await session.execute(stmt)
    # Distinct in case student appears multiple times (shouldn't with UniqueConstraint, but safe)
    students = result.scalars().unique().all()
    return students

# Fetch detailed enrollment listing for a course with status, optimized
async def get_enrollments_in_course(
    session, course_id: int, status: Optional[str]=None
) -> List[Enrollment]:
    stmt = select(Enrollment).where(Enrollment.course_id == course_id)
    if status:
        stmt = stmt.where(Enrollment.status == status)
    stmt = stmt.options(joinedload(Enrollment.student), joinedload(Enrollment.course))
    result = await session.execute(stmt)
    enrollments = result.scalars().all()
    return enrollments
