from sqlalchemy import (
    Column, Integer, String, ForeignKey, Enum, UniqueConstraint, Index
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum

Base = declarative_base()

class EnrollmentStatusEnum(str, enum.Enum):
    active = 'active'
    completed = 'completed'
    dropped = 'dropped'

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    enrollments = relationship('Enrollment', back_populates='student', cascade="all, delete-orphan")

    __table_args__ = (
        Index('ix_students_name', 'name'),
    )

class Course(Base):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    enrollments = relationship('Enrollment', back_populates='course', cascade="all, delete-orphan")

    __table_args__ = (
        Index('ix_courses_name', 'name'),
    )

class Enrollment(Base):
    __tablename__ = 'enrollments'
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id', ondelete='CASCADE'), nullable=False)
    course_id = Column(Integer, ForeignKey('courses.id', ondelete='CASCADE'), nullable=False)
    status = Column(Enum(EnrollmentStatusEnum), nullable=False, index=True)

    student = relationship('Student', back_populates='enrollments')
    course = relationship('Course', back_populates='enrollments')

    __table_args__ = (
        UniqueConstraint('student_id', 'course_id', name='uq_student_course'),
        Index('ix_enrollments_course_status', 'course_id', 'status'),
        Index('ix_enrollments_student_course', 'student_id', 'course_id'),
    )
