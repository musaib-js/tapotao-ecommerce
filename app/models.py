from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
STATE_CHOICES = (
  ('Andaman & Nicobar Islands','Andaman & Nicobar Islands'),
  ('Andhra Pradesh','Andhra Pradesh'),
  ('Arunachal Pradesh','Arunachal Pradesh'),
  ('Assam','Assam'),
  ('Bihar','Bihar'),
  ('Chandigarh','Chandigarh'),
  ('Chhattisgarh','Chhattisgarh'),
  ('Dadra & Nagar Haveli','Dadra & Nagar Haveli'),
  ('Daman and Diu','Daman and Diu'),
  ('Delhi','Delhi'),
  ('Goa','Goa'),
  ('Gujarat','Gujarat'),
  ('Haryana','Haryana'),
  ('Himachal Pradesh','Himachal Pradesh'),
  ('Jammu & Kashmir','Jammu & Kashmir'),
  ('Jharkhand','Jharkhand'),
  ('Karnataka','Karnataka'),
  ('Kerala','Kerala'),
  ('Lakshadweep','Lakshadweep'),
  ('Madhya Pradesh','Madhya Pradesh'),
  ('Maharashtra','Maharashtra'),
  ('Manipur','Manipur'),
  ('Meghalaya','Meghalaya'),
  ('Mizoram','Mizoram'),
  ('Nagaland','Nagaland'),
  ('Odisha','Odisha'),
  ('Puducherry','Puducherry'),
  ('Punjab','Punjab'),
  ('Rajasthan','Rajasthan'),
  ('Sikkim','Sikkim'),
  ('Tamil Nadu','Tamil Nadu'),
  ('Telangana','Telangana'),
  ('Tripura','Tripura'),
  ('Uttarakhand','Uttarakhand'),
  ('Uttar Pradesh','Uttar Pradesh'),
  ('West Bengal','West Bengal'),
)

class Customer(models.Model):
 user = models.ForeignKey(User, on_delete=models.CASCADE)
 name = models.CharField(max_length=200)
 locality = models.CharField(max_length=200)
 city = models.CharField(max_length=50)
 zipcode = models.IntegerField(('zipcode'), max_length=5,
   blank=True)
 state = models.CharField(choices=STATE_CHOICES, max_length=50)

 def __str__(self):
  # return self.user.username
  return str(self.id)


CATEGORY_CHOICES = (
 ('M', 'Mobile'),
 ('L', 'Laptop'),
 ('EL', 'Electronics'),
 ('HE', 'Hearing and Music'),
 ('WA', 'Watches'),
 ('TW', 'Top Wear'),
 ('BW', 'Bottom Wear'),
 ('BP', 'Beauty Products'),
 ('FW', 'Footwear'),
 ('KW', 'Kids Wear'),
 ('KC', 'Knitted Clothes'),
 ('FR', 'Frozen and Chilled'),
 ('B', 'Bakery'),
 ('CA', 'Car Accessories'),
 ('RF', 'Restaurant Food'),
 ('GR', 'Groceries'), 
 ('BK', 'Bakeries'),
 ('RF', 'Restaurant Food'),
 ('KS', 'Kashmiri Spices'),
 ('RP', 'Rice and Pulses'),
 ('DF', 'Dry Fruits')
)
class Product(models.Model):
 title = models.CharField(max_length=100)
 selling_price = models.FloatField()
 discounted_price = models.FloatField()
 description = models.TextField()
 brand = models.CharField(max_length=100)
 category = models.CharField( choices=CATEGORY_CHOICES, max_length=2)
 product_image = models.ImageField()

 def __str__(self):
  return str(self.id)

class Coupon(models.Model):
 title = models.CharField(max_length=100)
 worth = models.IntegerField()

 def __str__(self):
  return self.title

class bulk_order(models.Model):
  name= models.CharField(max_length=30)
  email= models.EmailField(max_length=254)
  contact_number=models.IntegerField(max_length=15)
  address= models.TextField(max_length=200)
  pin_code=models.IntegerField()
  details= models.TextField()
  
  def __str__(self):
   return self.name

class Cart(models.Model):
 user = models.ForeignKey(User, on_delete=models.CASCADE)
 product = models.ForeignKey(Product, on_delete=models.CASCADE)
 quantity = models.PositiveIntegerField(default=1)

 def __str__(self):
  return str(self.id)
  
  # Below Property will be used by checkout.html page to show total cost in order summary
 @property
 def total_cost(self):
   return self.quantity * self.product.discounted_price

STATUS_CHOICES = (
  ('Accepted','Accepted'),
  ('Being Processed', 'Being Processed'),
  ('Packed','Packed'),
  ('On The Way','On The Way'),
  ('Delivered','Delivered'),
  ('Cancel','Cancel')
)

class OrderPlaced(models.Model):
 user = models.ForeignKey(User, on_delete=models.CASCADE)
 customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
 product = models.ForeignKey(Product, on_delete=models.CASCADE)
 quantity = models.PositiveIntegerField(default=1)
 ordered_date = models.DateTimeField(auto_now_add=True)
 couponapplied = models.CharField(max_length = 150, default = "None")
 status = models.CharField(max_length=50,choices=STATUS_CHOICES,default='Pending')
 payment_screenshot = models.ImageField()

 class Meta:
  verbose_name_plural = "Orders Placed"

  # Below Property will be used by orders.html page to show total cost
 @property
 def total_cost(self):
   return self.quantity * self.product.discounted_price


class Ratings(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  rating = models.CharField(max_length=500)

  def __str__(self):
      return self.rating
  
  