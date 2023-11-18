from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseNotFound
from django.shortcuts import render
from django.template import loader
from django.urls import reverse
from .models import HouseList, SoldHouse, LoanAmount, ModelValidators


# Create your views here.
"""
make form for selling houses 
"""



def home(request): #index page / home page
    """
    should have link to page for selling houses and other methods in broker api
    """
    template = loader.get_template("houses/index.html")
    return HttpResponse(template.render())

def list_house(request):
    """
    retrieve house list from database and send query set
    """
    mydata = HouseList.objects.all()
    template = loader.get_template("houses/house_list.html")
    context = {
        'houselist' : mydata
    }

    if len(mydata) == 0: #if Houselist has no entries...
        return HttpResponse("There are currently no houses listed")
    else: #if Houselist has entries
        return HttpResponse(template.render(context, request))
        #return HttpResponse("wrong")

# def add_house(request):
#     """
#     Has post form for adding house entry
#     """
#     pass

def edit_house(request): #maybe same page as above and will check for ID to determine if edit action
    """
    Has 
    """
    template = loader.get_template("houses/edit_house.html")
    return HttpResponse(template.render(request=request))

def edit_process(request): #check ID if empty. Empty = Edit, Not Empty = Add
    """
    TODO should check if non voidable fields are not empty
    """   
    
    if ModelValidators.check_houselist(request.POST["location"],request.POST["developer"], (request.POST["price"])):
        return HttpResponseNotFound("Input is invalid.")

    if 'id' in request.POST: #ID data means EDIT house   #TODO Bad implementation 
        if request.POST['id']:
            house_data = HouseList.objects.get(pk=request.POST["id"])
            
            if 'location' in request.POST:
                if request.POST["location"]:
                    house_data.location_city = request.POST["location"]
            if 'developer' in request.POST:
                if request.POST["developer"]:
                    house_data.location_city = request.POST["developer"]
            if 'price' in request.POST:
                if request.POST["price"]:
                    house_data.location_city = request.POST["price"]
            if 'reserve' in request.POST:
                if request.POST["reserve"]:
                    if house_data.reserved is True:  #checks if house is already reserved
                        return HttpResponse("House is already reserved.", status = 409)
                    if request.POST["reserve"] == 'True':
                        reserve = True
                    else: 
                        reserve = False
                    house_data.reserved = reserve
            house_data.save()
            #return HttpResponse(house_data)
            return HttpResponseRedirect(reverse("houses:home"))

        else: #No ID data means ADD house
            
            HouseList.objects.create(location_city=request.POST["location"], developer=request.POST["developer"], price=int(request.POST["price"]))
            return HttpResponseRedirect(reverse("houses:home"))   #should redirect to sucess page and asks if they want to go to home

#remove_house.html
def remove_house(request): #can be merge with show house list and display the delete function there
    mydata = HouseList.objects.all()
    template = loader.get_template("houses/remove_house.html")
    context = {
        'houselist' : mydata
    }

    if len(mydata) == 0: #if Houselist has no entries...
        return HttpResponse("There are currently no houses listed")
    else: #if Houselist has entries
        return HttpResponse(template.render(context, request))
        #return HttpResponse("wrong")

#remove_house.html submit form
def remove_process(request):
    """
    receives list of house id(s) to be removed
    """
    #template = loader.get_template("houses/remove_house.html")
    for id in request.POST.getlist('remove'):
        house_data = HouseList.objects.get(pk=id)
        house_data.delete()


    return HttpResponseRedirect(reverse("houses:home"))  #should go to success page with redirect to home


def sell_house(request): #should have be able to hyperlink from a house listing and url should have id 
    template = loader.get_template("houses/sell_house.html") 
    return HttpResponse(template.render(request=request))


def sell_process(request):
    """
    create SoldHouse entry
    and process sell process
    if paid amount is less than price of house, create a loan database entry
    return error if no id, downpayment amount, financing option
    """
    dict_argument = {
        'id_of_house' : HouseList.objects.get(pk=request.POST['id']), #should use get or 404
        'downpayment_amount' : request.POST['downpayment_amount'],
        'financing_option' : request.POST['financing_option'],

    }   #dictionary containing arguments for create()
    if 'broker_name' in request.POST:
        if request.POST['broker_name']:  #so bad
            dict_argument['broker_name'] = request.POST['broker_name']
    if 'commission_percent' in request.POST:
        if request.POST['commission_percent']:

            if float(request.POST['commission_percent']) > 100:
                return HttpResponse("Commission percent is invalid.", status = 409)
            
            dict_argument['commission_percent'] = request.POST['commission_percent']

    
    house_data = HouseList.objects.get(pk=request.POST["id"])   
    if house_data.sold is True:  #checks if house is already reserved

        return get_error_page(request, error_message="House is already sold.", status_code=409)
    house_data.sold = True  #sets sold field to True
    house_data.save() 
    SoldHouse.objects.create(**dict_argument) #creates soldhouse entry

    if float(request.POST['downpayment_amount'] ) > float(house_data.price): #checks if downpayment is less or equal to price of house
        #breakpoint()
        
        return get_error_page(request, error_message="Amount paid is more than price of house.", status_code=409)
        
        
    
        

    
    if float(request.POST['downpayment_amount'] ) < float(house_data.price): #creates loanamount entry
        loanamount_dict = {
            'id_of_house' : HouseList.objects.get(pk=request.POST['id']),
            'original_amount' : float(house_data.price),
            'current_amount' : float(house_data.price) - float(request.POST['downpayment_amount']),


        }
        LoanAmount.objects.create(**loanamount_dict)
    return HttpResponseRedirect(reverse("houses:home"))
    

def get_error_page(request, error_message: str=None, status_code: int=None):
    #breakpoint()
    context = {
       'error_message' : error_message,
        }

    template = loader.get_template("houses/input_parameter_error.html")
    return HttpResponse(template.render(context, request), status = status_code)
    #return render(request, template_name=template, context=context, status=status_code)

