use shopping_cart;

create table products (
	serial_number int auto_increment PRIMARY KEY,
    product_name varchar(15) NOT NULL,
    quantity int NOT NULL,
    price float NOT NULL
);
insert into products (product_name, quantity, price) values
	('biscuits', 5, 20.50),
    ('cereals', 3, 90.00),
    ('chicken', 5, 100.00);

create table customer (
	customer_id int auto_increment PRIMARY KEY,
    customer_name varchar(25) NOT NULL,
    customer_address varchar(50) NOT NULL,
    customer_distance float NOT NULL
);

create table orders (
	order_num int auto_increment PRIMARY KEY,
    customer_id int,
	order_subtotal float,
    order_delivery float,
    FOREIGN KEY (customer_id) REFERENCES customer(customer_id)
);

create table order_item (
	order_item_id int auto_increment PRIMARY KEY,
    order_num int,
    serial_number int,
    quantity int,
    FOREIGN KEY (order_num) references orders(order_num),
	FOREIGN KEY (serial_number) references products(serial_number)
);

create table reference_table (
	reference_id int auto_increment PRIMARY KEY,
    reference_name varchar(50) NOT NULL,
    reference_value varchar(50) NOT NULL
);

insert into reference_table (reference_name, reference_value) values 
	('delivery_lower_threshold', '15'),
    ('delivery_upper_threshold', '30'),
    ('delivery_charge_near', '50'),
    ('delivery_charge_far', '100');