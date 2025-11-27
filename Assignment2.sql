-- Pre-break:
use classicmodels;
--1. Who are the top 5 sales representatives based on revenue generated?
select concat(employees.firstName, ' ', employees.lastName), sum(orderdetails.quantityOrdered * orderdetails.priceEach)
from employees inner join customers c on employees.employeeNumber = c.salesRepEmployeeNumber
join orders o on c.customerNumber = o.customerNumber
join orderdetails on o.orderNumber = orderdetails.orderNumber
group by employees.employeeNumber
order by sum(orderdetails.quantityOrdered * orderdetails.priceEach) desc
limit 5;

--2. Which product line generates the most revenue?
select productlines.productLine
from productlines inner join products p on productlines.productLine = p.productLine
join orderdetails o on p.productCode = o.productCode
group by productlines.productLine
order by sum(o.quantityOrdered * o.priceEach) desc
limit 1;
--3. Are there products that have never been sold?
select pr.productName, sum(o.quantityOrdered)
from products pr inner join orderdetails o on pr.productCode = o.productCode
group by pr.productCode
having sum(o.quantityOrdered) = 0;
--No, it looks like all products have at least 1 order
--4. How many orders were placed per month in the last year? (Assumng it is 2005/6 since that's the last year in the DB)
select count(orderNumber), substr(orderDate, 1, 7)
from orders
where substr(orderDate, 1, 4) = '2005'
group by substr(orderDate, 1, 7);
--5. What are the most frequently ordered products?
select pr.productName, sum(o.quantityOrdered)
from products pr inner join orderdetails o on pr.productCode = o.productCode
group by pr.productCode
having sum(o.quantityOrdered) != 0
order by sum(o.quantityOrdered) desc;

use challenge1;
-- 1. What is the total amount each customer spent at the restaurant?
select s.customer_id, sum(m.price)
from sales s inner join menu m on s.product_id = m.product_id
group by s.customer_id;
-- 2. How many days has each customer visited the restaurant?
select s.customer_id, count(s.order_date)
from sales s
group by s.customer_id;
-- 3. What was the first item from the menu purchased by each customer?
select distinct s.customer_id, s.order_date
from (
	select customer_id, order_date,
           rank() over (partition by customer_id order by order_date asc) as rnk
    from sales
) as s
where s.rnk = 1;
-- 4. What is the most purchased item on the menu and how many times was it purchased by all customers?
select s.product_id, count(s.customer_id) as purchases
from sales s
group by s.product_id;
-- 5. Which item was the most popular for each customer?
# Change row_number to rank to get the ties for customer B.
select s.customer_id, s.product_id, orders
from (
	select customer_id, product_id, count(product_id) as orders,
		   row_number() over (partition by customer_id order by count(product_id) desc) as rnk
    from sales
    group by customer_id, product_id
    order by product_id desc
) as s
where rnk = 1
order by customer_id, product_id;
-- 6. Which item was purchased first by the customer after they became a member?
select s.customer_id, s.product_id, s.order_date
from (select s.customer_id, s.product_id, s.order_date,
		row_number() over (partition by s.customer_id order by s.order_date) as rnk
	  from sales s inner join members m on s.customer_id = m.customer_id
	  where s.order_date > m.join_date
	  order by s.order_date asc
) as s
where rnk = 1;
-- 7. Which item was purchased just before the customer became a member?
select s.customer_id, s.product_id, s.order_date
from (select s.customer_id, s.product_id, s.order_date,
		row_number() over (partition by s.customer_id order by s.order_date desc) as rnk
	  from sales s inner join members m on s.customer_id = m.customer_id
	  where s.order_date < m.join_date
	  order by s.order_date asc
) as s
where rnk = 1;
-- 8. What is the total items and amount spent for each member before they became a member?
select sale.customer_id, count(sale.product_id), sum(sale.price)
from (select s.customer_id, s.product_id, me.price,
		row_number() over (partition by s.customer_id order by s.order_date desc) as rnk
	  from sales s inner join members m on s.customer_id = m.customer_id
           join menu me on s.product_id = me.product_id
	  where s.order_date < m.join_date
	  order by s.order_date asc
) as sale
group by sale.customer_id;
-- 9.  If each $1 spent equates to 10 points and sushi has a 2x points multiplier - how many points would each customer have?
select s.customer_id, sum(m.price * 10 * CASE WHEN s.product_id = 1 then 2 ELSE 1 END)
from sales s inner join menu m on s.product_id = m.product_id
group by s.customer_id;
-- 10. In the first week after a customer joins the program (including their join date) they earn 2x points on all items, not just sushi - how many points do customer A and B have at the end of January?
select s.customer_id, 
	   sum(m.price * 10 * CASE WHEN s.product_id = 1 then 2 ELSE 1 END * CASE WHEN s.order_date >= me.join_date and DATEDIFF(s.order_date, me.join_date) <= 7 then 2 ELSE 1 END)
from sales s inner join menu m on s.product_id = m.product_id
     join members me on s.customer_id = me.customer_id
where s.order_date < '2021-02-01'
group by s.customer_id;

use classicmodels;
--Q1 : Write a query using a CTE to find the top 5 customers who have made the highest total payment amount.
with CTE_Q1 as (
    select c.customerName, sum(od.quantityOrdered * od.priceEach) as payment,
		   row_number() over (order by sum(od.quantityOrdered * od.priceEach) desc) as rnk
    from customers c inner join orders o on c.customerNumber = o.customerNumber
	     join orderdetails od on o.orderNumber = od.orderNumber
	group by c.customerName
)
SELECT output.customerName, output.payment
from CTE_Q1 as output
where output.rnk <= 5;
--Q2 : Write a query using a CTE to calculate how many customers each employee (sales rep) manages.
with CTE_Q2 as (
	SELECT salesRepEmployeeNumber, count(customerNumber) as manageCount
    from customers
    where salesRepEmployeeNumber is not null
    group by salesRepEmployeeNumber
    order by manageCount
)
SELECT concat(firstName, ' ', lastName), output.manageCount
FROM CTE_Q2 as output inner join employees e on output.salesRepEmployeeNumber = e.employeeNumber;
