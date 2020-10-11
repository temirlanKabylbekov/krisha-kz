CREATE TABLE flats (
	krisha_id INT,
	title TEXT,
	url VARCHAR (255),
	pub_date DATE,
	views_count INT,
	seller_phone VARCHAR (255),
	price NUMERIC (14,2),
	rooms_count INT,
	total_area NUMERIC (14,2),
	ceiling_height NUMERIC (14,2),
	region VARCHAR (255),
	city VARCHAR (255),
	address TEXT,
	flat_floor INT,
	longitude NUMERIC (14,8),
	attitude NUMERIC (14,8),
	construction_year INT,
	floors_count INT,
	wall_type VARCHAR (255),
	seller_user_type VARCHAR (255),
	parsed_date DATE
);
