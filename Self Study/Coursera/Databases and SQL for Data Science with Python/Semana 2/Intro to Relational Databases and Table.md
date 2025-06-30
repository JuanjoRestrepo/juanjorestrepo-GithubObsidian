---
tags:
  - Coursera
  - SelfLearning
  - Study
  - SQL
  - DataBases
---

# Information Model and Data Models
---
## 1. Relational Model
---
- Most used data model
- Allows for data independence
- Data is stored in a simple data structure. Tables: this provides logical data independence, physical data independence, and physical storage independence.

An **entity relationship** data model, or **ER data model**, is an alternative to a relational data model.

Using a simplified library database as an example, this  figure shows an entity relationship diagram or ERD that represents entities called tables and their relationships.

![[Pasted image 20231127183702.png]]

*In the library example, we have books. A book can be written by one or many authors. The library can have one or many copies of a book. Each copy can be borrowed by only one borrower at a time.*

**An entity relationship model** proposes thinking of a database as a **collection of entities** rather than being used as a model on its own.

## Entity-Relationship Model
---
- Used as a tool to design relational databases

Using a simplified library database as an example, this  figure shows an entity relationship diagram or ERD that represents entities called tables and their relationships.

![[Pasted image 20231127184019.png]]

In an ER diagram, attributes are drawn as ovals. Using a simplified library as an example, the book is an example of an entity. 
- Attributes are certain properties or characteristics of an entity and tell us more about the entity. 
- The entity book has attributes such as book title, the edition of the book, the year the book was written, etc
- Attributes are connected to exactly one entity.
- **The entity book becomes a table** in the database and the **attributes become the columns** in a table

## Mapping Entity Diagrams to Tables
---
- Entities become tables
- Attributes get translated into columns
- Each attribute stores data values of different formats, characters, numbers dates, currency, and many more besides

![[Pasted image 20231127184455.png]]
- As book titles vary in length, we can set the variable character data type for the title column: VAR char.
- The Edition and year columns would be numeric.
- The ISBN column would be carved because it contains dashes as well as numbers and so on.

## Primary Keys and Foreign Keys
---
![[Pasted image 20231127184709.png]]

Each table is assigned a primary. he primary key of a relational table uniquely identifies each tuple or row in a table, preventing duplication of data and providing a way of defining relationships between tables.

 Tables can also contain **foreign keys** which are primary keys defined in other tables, creating a link between the tables.

### Summary
---
- The key advantage of the relational model is data independence
- Entities are independent objects which have **Attributes**
- Entities map to Tables in a Relational Database
- Attributes map to Columns in a Table
- Common data types include characters, numbers and dates/times.
- A Primary Key uniquely identifies a specific row in a table

