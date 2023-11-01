# Overview
Storage is the special directory that includes all valuable information for the bot to run. The storage is entitled be unique for each distribution of this project.
# Structure
- `subjects/` All studied subjects of that distribution.
- `subjects/subject` Information for specific subject.
- `subjects/subject/files/` Shared files for that subject.
- `subjects/subject/assignments.csv` Assignments for that subject. 
  - **format**: date, type, author, approved
- `students.csv` All students of that distribution.
  - **format**: id, name, permission, date
