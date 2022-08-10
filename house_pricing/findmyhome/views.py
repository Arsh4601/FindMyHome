from multiprocessing import context
from django.shortcuts import render
from django.contrib import messages
import numpy as np
import joblib
from findmyhome.models import Feedback
from datetime import date
# Create your views here.

def home(request):

    if request.method=="POST": #print("If form request")

        #print("Retrieving input values")

        ovqual=request.POST.get("overalqual")
        carcap=request.POST.get("carcap")
        garagecar=request.POST.get("garagecar")
        yrbuilt=request.POST.get("yrbuilt")
        livarea=request.POST.get("livarea")
        totalbsmt=request.POST.get("totalbsmt")
        remodedate=request.POST.get("remodedate")
        mstype=request.POST.get("mstype")

        #print("Checking for empty fields")

        if(ovqual=="" or carcap=="" or garagecar=="" or yrbuilt=="" or livarea=="" or totalbsmt=="" or remodedate=="" or mstype==""):

            #print("Penalizing for empty fields")

            messages.warning(request, 'Please fill all fields of the form')
            return render(request,"home.html")
        
        #print("Typecasting int input values")
        else:

            try: #print("Checking for invalid values")

                ovqual=int(ovqual)

                                
                
                carcap=int(carcap)

                
                
                garagecar=int(garagecar)

                
                
                yrbuilt=int(yrbuilt)



                livarea=int(yrbuilt)



                totalbsmt=int(totalbsmt)



                remodedate=int(remodedate)


                #print("Creating sessions for input values")

                request.session["ovqual"]=ovqual



                request.session["carcap"]=carcap



                request.session["garagecar"]=garagecar



                request.session["yrbuilt"]=yrbuilt



                request.session["livarea"]=livarea



                request.session["totalbsmt"]=totalbsmt



                request.session["remodedate"]=remodedate



                request.session["mstype"]=mstype

                #print("Calling for return view")

                return result(request)

            except: #print("Penalizing for invalid values")

              messages.warning(request, 'Please fill all fields of the form approraitely')
              return render(request,"home.html")




    else: #print("If no form request")

        
        return render(request,"home.html")




def result(request):


    #print("Retrieving session variables")

    ovqual=request.session["ovqual"]
    
    
    carcap=request.session["carcap"]
    
    
    garagecar=request.session["garagecar"]
    
    
    yrbuilt=request.session["yrbuilt"]
    
    
    livarea=request.session["livarea"]
    

    
    totalbsmt=request.session["totalbsmt"]
    
    
    remodedate=request.session["remodedate"]
    
    
    mstype=request.session["mstype"]    

   #print("Preparing x array for result.html")
    
    x=[ovqual,carcap,garagecar,yrbuilt,livarea,totalbsmt,remodedate,mstype]
    
    #print("Initializing model/scales")

    sc=joblib.load('C:/Users/Arsh/Desktop/django Project/house_pricing/static/ml model/standardsc.pkl')
    minmax=joblib.load('C:/Users/Arsh/Desktop/django Project/house_pricing/static/ml model/minmaxsc.pkl')
    lr=joblib.load('C:/Users/Arsh/Desktop/django Project/house_pricing/static/ml model/price.pkl')
    le=joblib.load('C:/Users/Arsh/Desktop/django Project/house_pricing/static/ml model/labelenc.pkl')


   # print("label encoding")

    amstype=[mstype]

    con_mstype=le.transform(amstype)[0]   

    #print("preparing x_test")

    ps_x=np.array([[ovqual],[carcap],[garagecar],[yrbuilt],[livarea],[totalbsmt],[con_mstype],[remodedate]])


    #print("reshaping x_test")

    ps_x=ps_x.reshape(1,-1)


    #print("Standardizing x_test")


    ps_xstd=sc.transform(ps_x)    


    #print("Predicting y_pred")

    ps_ypred=lr.predict(ps_xstd)

    
    #print("Reconverting y_pred")

    ps_ypred=minmax.inverse_transform(ps_ypred)    

    ans=ps_ypred[0]

    print("Printing x_test and y_pred")
    

    context={"x":x, "price":round(ans[0],2)}     

    
    return render(request,"result.html",context=context)




def about(request):

    return render(request,"about.html")
    

def feed(request):

    if request.method=="POST": #print("If form request")

        #print("Reteriving form values")

        name=request.POST.get("name")
        email=request.POST.get("email")
        feed=request.POST.get("feed")
        
        if(name=="" or email=="" or feed==""):#print("Check for empty fields")

            #print("Penalizing for empty fields")
            messages.warning(request, 'Please fill all fields of the form')
            return render(request,"feedback.html")

        else:

            #print("Validating name")

            try:

                name=int(name)
                sname=1
                messages.warning(request, 'Please fill correct name')
                return render(request,"feedback.html")

            except:


                try:

                    name=float(name)
                    sname=1
                    messages.warning(request, 'Please fill correct name')
                    return render(request,"feedback.html")

                except:

                    sname=0

            #print("Validating email")

            flag=0

            if("a"<=email[0]<="z" or  "A"<=email[0]<="Z" ):



                for i in range(1,len(email)):

                    if("a"<=email[i]<="z" or  "A"<=email[i]<="Z" ):



                        continue

                    elif("0"<=email[i]<="9"):


                        continue

                    else:

                        if(email[i]=="@"):


                            flag=0
                            break

                        elif(email[i]=="."):

                            continue

                        else:

                            flag=1

                            break
            else:

                flag=1


            if(flag==0):

                substr=email[i:len(email)]
                if(substr=="@gmail.com" or substr=="@gmail.co.in" or substr=="@email.com"):


                    semail=0

                else:

                    semail=1

                    messages.warning(request, 'Please enter approriate email')
                    return render(request,"feedback.html")


            else:

                semail=1
                messages.warning(request, 'Please enter approriate email')
                return render(request,"feedback.html")

            #print("Validating Feedback")

            try:

                feed=int(feed)
                sfeed=1
                messages.warning(request, 'Please give approriate feedback')
                return render(request,"feedback.html")

            except:

                try:

                    feed=float(feed)
                    sfeed=1
                    messages.warning(request, 'Please give approriate feeedback')
                    return render(request,"feedback.html")

                except:

                    sfeed=0


            if(sname==0 and semail==0 and sfeed==0): #print("Check if all the fields are valid ")

                messages.success(request, 'Thank you for your response, we will get back to you soon')

                #print("Store Feedback in database")

                cdate=date.today()

                f=Feedback(date=cdate,name=name,email=email,comment=feed)
                f.save()

                return render(request,"feedback.html")


    else:#print("If no form request")

        return render(request,"feedback.html")


