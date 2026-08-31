
# Practice Quiz
---
#### Question 1
How many albums does the artist Led Zeppelin have?
```SQL
SELECT Name, Count(name) as total
From artists as ar
Join albums as al on ar.artistid = al.artistid
Where name = 'Led Zeppelin'
Group by name
```

#### Question 2
Create a list of album titles and the unit prices for the artist "Audioslave".
```SQL
Select ar.Name, title, UnitPrice
From albums as al
Join artists as ar on ar.artistid = al.artistid
Join tracks as tr on tr.albumid = al.albumid
Where ar.Name = 'Audioslave'
```

#### Question 3
Find the first and last name of any customer who does not have an invoice. Are there any customers returned from the query?
```SQL
Select FirstName, LastName, Invoiceid
From customers
Join invoices USING (Customerid)
Where Invoiceid is null
```

#### Question 4
Find the total price for each album.
```SQL
Select title, UnitPrice, Sum(UnitPrice) AS TotalPrice
From albums as al
Join artists as ar on ar.artistid = al.artistid
Join tracks as tr on tr.albumid = al.albumid
Where Title ='Big Ones'
Group By Title
```

#### Question 5
How many records are created when you apply a Cartesian join to the invoice and invoice items table?
```SQL
select invoices.InvoiceId
from invoices cross join invoice_items
```


# Final Quiz
---

1. Using a subquery, find the names of all the tracks for the album "Californication".
```SQL
Select name, Albumid
From Tracks
Where Albumid = (Select Albumid from Albums
Where title = 'Californication')
```


2. Find the total number of invoices for each customer along with the customer's full name, city and email.
```SQL
Select FirstName, LastName, City, Email, Customerid, Count(*) 
From Customers 
Where Customerid IN (Select Customerid From Invoices
Where Customers.Customerid = Invoices.Customerid)
Group by Email
Having FirstName = 'František'
```
 
 3. Retrieve the track name, album, artistID, and trackID for all the albums.
 What is the song title of trackID 12 from the "For Those About to Rock We Salute You" album? Enter the answer below.
```SQL
Select Name, title, ArtistId, TrackId
From Albums AS al 
Left Join Tracks AS tr ON  tr.AlbumId = al.AlbumId 
Group by Name
Having TrackId = 12
```

4. Retrieve a list with the managers last name, and the last name of the employees who report to him or her.
```SQL
Select B.LastName AS Managers,A.LastName AS EmpName
From Employees A,Employees B
Where A.ReportsTo = B.EmployeeId
Order By Managers 
```

5. Find the name and ID of the artists who do not have albums.
```SQL
Select ArtistId, Name
From Artists
Where ArtistId Not IN (Select ArtistId From Albums)
```

6. Use a UNION to create a list of all the employee's and customer's first names and last names ordered by the last name in descending order. After running the query described above, determine what is the last name of the 6th record? Enter it below. Remember to order things in descending order to be sure to get the correct answer.
```SQL
Select FirstName, LastName
From Employees
UNION
Select FirstName, LastName
From Customers
Order By LastName DESC
```

7. See if there are any customers who have a different city listed in their billing city versus their customer city.
```SQL
Select City From Customers
Where City NOT IN (Select BillingCity From Invoices)
```


# Module 3 Quiz
---

1. Which of the following statements is true regarding subqueries?
  <p>  Subqueries always process the innermost query first and the work outward.  </p>
 
2. If you can accomplish the same outcome with a join or a subquery, which one should you always choose?<
<p>	Joins are usually faster, but subqueries can be more reliable, so it depends on your situation.</p>

3. The following diagram is a depiction of what type of join? 
<p>Inner Join</p>

4. Select which of the following statements are true regarding inner joins. (Select all that apply).</h5></p>
<p>  Inner joins are one of the most popular types of joins use </p>
<p>  There is no limit to the number of table you can join with an inner join.  </p>
<p>	Performance will most likely worsen with the more joins you make </p>

5. Which of the following is true regarding Aliases?
<p>  Aliases are often used to make column names more readable.  </p>
<p> SQL aliases are used to give a table, or a column in a table, a temporary name.  </p>
<p> An alias only exists for the duration of the query. </p>

6. What is wrong with the following query?

```SQL
SELECT Customers.CustomerName, Orders.OrderID

FROM LEFT JOIN ON Customers.CustomerID = Orders.CustomerID FROM Orders AND Customers

ORDER BY

CustomerName;
```

<p> Should be using an inner join rather than a left join  </p>
<p>  Column names do not have an alias  </p>


7. What is the difference between a left join and a right join?.
<p>  The only difference between a left and right join is the order in which the tables are relating.  </p>

 8. If you perform a cartesian join on a table with 10 rows and a table with 20 rows, how many rows will there be in the output table?</h5></p>
<p> 200 </p>

9. Which of the following statements is true? (select all that apply).
<P> Each SELECT statement within UNION must have the same number of columns  </p>
<p> The UNION operator is used to combine the result-set of two or more SELECT statements </p>
<p> The columns must also have similar data types </p>


10. Data scientists need to use joins in order to: (select the best answer)
<p>  Retrieve data from multiple tables. </p>