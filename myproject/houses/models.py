from django.db import models

# Create your models here.

class HouseList(models.Model):
    location_city = models.CharField(max_length=200)
    developer = models.CharField(max_length=200)
    price = models.IntegerField(default=0)
    reserved = models.BooleanField(default=False, null=True)
    sold = models.BooleanField(default=False, null=True)

    def is_reserved(self):
        if self.reserved is True:
            return True
        else:
            return False
    
    def is_sold(self):
        if self.sold is True:
            return True
        else:
            return False



    def __str__(self):
        return str(self.pk)
    # Sold_Houses: Mapped[List["SoldHouses"]] = relationship(back_populates="House")
    # loan_record: Mapped[List["LoanAmount"]] = relationship(back_populates="house_record")
    #TODO add is reserved and is sold methods to model 

class SoldHouse(models.Model):
    id_of_house = models.ForeignKey(HouseList, on_delete=models.CASCADE)
    broker_name = models.CharField(max_length=200, null=True)
    commission_percent = models.CharField(max_length=200, null=True)
    downpayment_amount = models.FloatField(default=0)   
    financing_option = models.CharField(max_length=200, default=None)
    #House: Mapped[List["HouseList"]] = relationship(back_populates="Sold_Houses")


class LoanAmount(models.Model):
    id_of_house = models.ForeignKey(HouseList, on_delete=models.PROTECT) #loan record should be kept even if house entry is deleted 
    original_amount = models.FloatField()
    current_amount = models.FloatField()
    #house_record: Mapped[List["HouseList"]] = relationship(back_populates="loan_record")

class ModelValidators:

    @staticmethod
    def check_houselist(location=None, developer=None, price=0): #checks if inputs are valid. price should be greater than zero. 
        if location:
            if not isinstance(location, str): #if not str return false
                return True
            
        if developer:
            if not isinstance(developer, str): #if not str return false
                return True
            
        if price:
            try:
                if int(price) <= 0:
                    pass
            except ValueError:
                return True

        return False #returns false if all guard clauses pass

