CREATE TABLE "Bill" (
	"Bill_id" serial(50) NOT NULL,
	"Bill_amount" double(50) NOT NULL,
	"User_id" serial(50) NOT NULL,
	"Rest_id" serial(50) NOT NULL,
	CONSTRAINT "Bill_pk" PRIMARY KEY ("Bill_id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "Customer" (
	"User_id" serial(50) NOT NULL,
	"Customer_name" character(50) NOT NULL,
	"C_Email" character(50) NOT NULL UNIQUE,
	"C_Phone" int(50) NOT NULL UNIQUE,
	"C_Location" character(200) NOT NULL,
	CONSTRAINT "Customer_pk" PRIMARY KEY ("User_id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "Restaurant" (
	"Rest_id" serial(50) NOT NULL,
	"R_Name" character(50) NOT NULL UNIQUE,
	"R_Description" character(200) NOT NULL,
	"R_Location" character(200) NOT NULL,
	"R_OpenTime" TIME(200) NOT NULL,
	"R_Contact" serial(200) NOT NULL UNIQUE,
	"R_Img" serial(200) NOT NULL UNIQUE,
	CONSTRAINT "Restaurant_pk" PRIMARY KEY ("Rest_id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "Menu" (
	"Menu_id" serial(50) NOT NULL,
	"img" serial(50) NOT NULL,
	"name" character(50) NOT NULL,
	"price" double(50) NOT NULL,
	"ratings" double(10) NOT NULL,
	"description" TEXT(50) NOT NULL,
	"Rest_id" character(50) NOT NULL,
	"Category_id" character(50) NOT NULL,
	CONSTRAINT "Menu_pk" PRIMARY KEY ("Menu_id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "Category" (
	"Category_id" serial(50) NOT NULL,
	"Category_name" TEXT(50) NOT NULL,
	CONSTRAINT "Category_pk" PRIMARY KEY ("Category_id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "Manager" (
	"Maneger_id" serial(50) NOT NULL,
	"User_name" serial(50) NOT NULL,
	"M_Email" serial(50) NOT NULL UNIQUE,
	"M_Phone" serial(50) NOT NULL UNIQUE,
	"Rest_id" serial(50) NOT NULL,
	"User_type" serial(50) NOT NULL,
	CONSTRAINT "Manager_pk" PRIMARY KEY ("Maneger_id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "Users" (
	"User_type" serial(50) NOT NULL,
	CONSTRAINT "Users_pk" PRIMARY KEY ("User_type")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "Order" (
	"Order_id" serial(40) NOT NULL,
	"User_id" serial(50) NOT NULL,
	"Quantity" int(50) NOT NULL,
	"Menu_id" character(50) NOT NULL,
	CONSTRAINT "Order_pk" PRIMARY KEY ("Order_id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "Ratings" (
	"Ratings_id" serial NOT NULL,
	"Menu_id" serial(50) NOT NULL,
	CONSTRAINT "Ratings_pk" PRIMARY KEY ("Ratings_id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "Login" (
	"Email" serial(50) NOT NULL,
	"Username" serial(50) NOT NULL,
	"User_type" serial(50) NOT NULL,
	CONSTRAINT "Login_pk" PRIMARY KEY ("Email")
) WITH (
  OIDS=FALSE
);



ALTER TABLE "Bill" ADD CONSTRAINT "Bill_fk0" FOREIGN KEY ("User_id") REFERENCES "Customer"("User_id");
ALTER TABLE "Bill" ADD CONSTRAINT "Bill_fk1" FOREIGN KEY ("Rest_id") REFERENCES "Restaurant"("Rest_id");



ALTER TABLE "Menu" ADD CONSTRAINT "Menu_fk0" FOREIGN KEY ("Rest_id") REFERENCES "Restaurant"("Rest_id");
ALTER TABLE "Menu" ADD CONSTRAINT "Menu_fk1" FOREIGN KEY ("Category_id") REFERENCES "Category"("Category_id");


ALTER TABLE "Manager" ADD CONSTRAINT "Manager_fk0" FOREIGN KEY ("Rest_id") REFERENCES "Restaurant"("Rest_id");
ALTER TABLE "Manager" ADD CONSTRAINT "Manager_fk1" FOREIGN KEY ("User_type") REFERENCES "Users"("User_type");


ALTER TABLE "Order" ADD CONSTRAINT "Order_fk0" FOREIGN KEY ("User_id") REFERENCES "Customer"("User_id");
ALTER TABLE "Order" ADD CONSTRAINT "Order_fk1" FOREIGN KEY ("Menu_id") REFERENCES "Menu"("Menu_id");

ALTER TABLE "Ratings" ADD CONSTRAINT "Ratings_fk0" FOREIGN KEY ("Menu_id") REFERENCES "Menu"("Menu_id");

ALTER TABLE "Login" ADD CONSTRAINT "Login_fk0" FOREIGN KEY ("User_type") REFERENCES "Users"("User_type");

