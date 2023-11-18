from django.test import TestCase, Client
from django.urls import reverse
from houses.models import HouseList, SoldHouse, LoanAmount

# Create your tests here.






class ModelsTests(TestCase):
    def test_houselist_model_is_reserved_method_works(self): #TODO
        house = HouseList()
        house.reserved = True
        self.assertEqual(house.is_reserved(), True)
    
    def test_houselist_model_is_sold_method_works(self): #TODO
        house = HouseList()
        house.sold = True
        self.assertEqual(house.is_sold(), True)

    def test_this(self):
        house = HouseList()
        house.price = 'asd'
        self.assertEqual(house.price, 'asd')






def create_houselist(location, developer, price, reserved=False):
    return HouseList.objects.create(location_city=location, developer=developer, price=int(price))

class BrokerOperationsTests(TestCase):
    def test_should_check_if_houselist_parameters_are_valid(self): #when creating a houselist entry the parameters should be correct
        houselist_data = {
            'id' : '',
            'location' : 'test',
            'developer' : 'test',
            'price' : '123',

        }
        response = self.client.post(reverse('houses:edit_process'), houselist_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")

    def test_should_return_error_if_create_houselist_parameters_are_invalid(self):
        houselist_data = {
            'id' : '',
            'location' : 'test',
            'developer' : 'test',
            'price' : 'as',

        }
        response = self.client.post(reverse('houses:edit_process'), houselist_data)
        self.assertContains(response, "Input is invalid.", status_code=404)

    def test_edit_process_should_be_able_to_create_houselist_entry(self): #integration test
        house1 = create_houselist("test", "test", 100)
        house_retrieved = HouseList.objects.get(pk=1)
        self.assertEqual(house1, house_retrieved)
        self.assertEqual(house1.developer, house_retrieved.developer)
        self.assertEqual(house1.location_city, house_retrieved.location_city)
        
    def test_houselist_entry_to_be_edited_should_exist(self): #??? what is this test
        create_houselist("test", "test", 100) 
        houselist_data = {
        'id' : '1',
        'location' : 'test',
        'developer' : 'test',
        'price' : '100',
        }
        response = self.client.post(reverse('houses:edit_process'), houselist_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")

    def test_house_reserve_the_house_in_the_database(self): #TODO #integration test
        create_houselist("test", "test", 100) 
        houselist_data = {
        'id' : '1',
        'location' : 'test',
        'developer' : 'test',
        'price' : '100',
        'reserve' : 'True'
        }
        response = self.client.post(reverse('houses:edit_process'), houselist_data)
        house_retrieved = HouseList.objects.get(pk=1)
        self.assertEqual(True, house_retrieved.reserved)

        


    def test_house_can_only_be_reserved_once(self): #TODO
        create_houselist("test", "test", 100) 
        houselist_data = {
        'id' : '1',
        'location' : 'test',
        'developer' : 'test',
        'price' : '100',
        'reserve' : 'True'
        }
        response = self.client.post(reverse('houses:edit_process'), houselist_data)
        response = self.client.post(reverse('houses:edit_process'), houselist_data) #reserve house twice
        self.assertContains(response, "House is already reserved.", status_code=409)

        
    
    def test_remove_house_should_be_able_to_remove_houselist_entries_from_database(self): #think of better way to check if delete operation succeeded
        house1 = create_houselist("test", "test", 100)
        houselist_data = {
            'remove' : 1
        }

        response = self.client.post(reverse('houses:remove_process'), houselist_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")

    def test_remove_house_should_be_able_to_remove_multiple_houselist_entries_from_database(self): # more than 1 entry to be deleted
        house1 = create_houselist("test", "test", 100)
        house2 = create_houselist("test", "test", 100)
        house3 = create_houselist("test", "test", 100)
        houselist_data = {
            'remove' : [1,2,3]
        }

        response = self.client.post(reverse('houses:remove_process'), houselist_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")

    def test_sell_houses_operation_updates_sold_field_to_true(self): #this test create a database entry that needs to be retrieved 
        house1 = create_houselist("test", "test", 100)
        houselist_data = {
            'id' : house1,
            'financing_option' : 'test',
            'downpayment_amount' : 100,
            'broker_name' : 'Test',
            'commission_percent' : 100
        }

        response = self.client.post(reverse('houses:sell_process'), houselist_data)
        house_database_retrieved_data = HouseList.objects.get(pk=1)
        self.assertEqual(house_database_retrieved_data.sold, True)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")

    def test_houses_can_only_be_sold_once(self): 
        house1 = create_houselist("test", "test", 100)
        houselist_data = {
            'id' : house1,
            'financing_option' : 'test',
            'downpayment_amount' : 100,
            'broker_name' : 'Test',
            'commission_percent' : 100
        }
        response = self.client.post(reverse('houses:sell_process'), houselist_data)
        response = self.client.post(reverse('houses:sell_process'), houselist_data) #sell the same house twice 
        self.assertContains(response, "House is already sold.", status_code=409)
    
    def test_price_paid_should_be_less_than_price_of_house(self):
        house1 = create_houselist("test", "test", 100)
        houselist_data = {
            'id' : house1,
            'financing_option' : 'test',
            'downpayment_amount' : 100.1,
            'broker_name' : 'Test',
            'commission_percent' : 100
        }
        response = self.client.post(reverse('houses:sell_process'), houselist_data)
        self.assertContains(response, "Amount paid is more than price of house.", status_code=409)

    def test_commission_percent_should_only_reach_up_to_100(self):
        house1 = create_houselist("test", "test", 100)
        houselist_data = {
            'id' : house1,
            'financing_option' : 'test',
            'downpayment_amount' : 100,
            'broker_name' : 'Test',
            'commission_percent' : 100.1
        }
        response = self.client.post(reverse('houses:sell_process'), houselist_data)
        self.assertContains(response, "Commission percent is invalid.", status_code=409)
    






class ViewDisplayTests(TestCase):
    def test_view_list_house_should_be_able_to_handle_having_no_database_entries(self): #list_house

        response = self.client.get(reverse('houses:list_house'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are currently no houses listed")
    
    def test_view_list_house_display_houses_in_database(self):
        #create_houselist(location, developer, price)
        house1 = create_houselist("test", "test", 100)
        house2 = create_houselist("test", "test", 100)
        response = self.client.get(reverse('houses:list_house'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context["houselist"], [house1, house2], ordered=False)

    # def test_home_view_should_(self):
    #     house = HouseList()
    #     house.id = 1
    #     self.assertEqual(house.id, 1)
    
    def test_remove_house_with_no_house_listed_should_return_expected_response(self):
        response = self.client.get(reverse('houses:remove_house'))
        self.assertContains(response, "There are currently no houses listed", status_code=200)

    def test_multiple_houselist_entries_should_appear_in_remove_house_page(self):
        house1 = create_houselist("test", "test", 100)
        house2 = create_houselist("test", "test", 100)
        house3 = create_houselist("test", "test", 100)
        response = self.client.get(reverse('houses:remove_house'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context["houselist"], [house1, house2, house3], ordered=False)
