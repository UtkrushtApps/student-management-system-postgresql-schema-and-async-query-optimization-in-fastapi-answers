# Solution Steps

1. Refactor the database schema to include foreign keys on enrollments (student_id -> students.id, course_id -> courses.id), ensuring referential integrity.

2. Ensure uniqueness of (student_id, course_id) pairs in the enrollments table using a UniqueConstraint.

3. Add indexes on the columns and column combinations most frequently used in queries: student_id, course_id, status, and (course_id, status), as well as (student_id, course_id) to assist join/filter performance.

4. In the Student and Course models, add indexes on 'name' columns for potential search optimization.

5. In the async query for listing students enrolled in a course (optionally filtered by status), use an explicit JOIN to Enrollment and push all filters into the WHERE clause so that indexes are used properly.

6. Use SQLAlchemy's joinedload on relationships to minimize extra queries and support eager loading.

7. Optimize the enrollment listing query similarly: eager load related student and course, filter on indexed columns.

8. Write all logic in the data/query layer only; do not modify FastAPI routes or openapi schema.

9. Ensure queries use .unique(), as needed, to avoid returning duplicate students in the rare case of inconsistent data.

10. Test the queries with realistic datasets and ensure response times remain low even as data grows.

