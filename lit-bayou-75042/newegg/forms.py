"""forms.py"""
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.core import serializers
from django.core.mail import send_mail
from .models import Document, Product, Client
from . import models
from ftplib import FTP
import os, pandas, uuid, json
from celery import signature, group
from tasks import file_upload, send_email

class RegistrationForm(forms.ModelForm):
    registeremail = forms.EmailField(required = True)
    registerusername = forms.CharField(required = True)
    registerpassword1 = forms.CharField(required = True)
    registerpassword2 = forms.CharField(required = True)
    phone = forms.CharField(required = True)
    registerseller_id = forms.CharField(required = True)
    registerauthorization = forms.CharField(required=True)
    

    class Meta:
        model = User
        fields = {'registerusername','registerpassword1', 'registerpassword2', 'registeremail', 
                'phone','registerseller_id','registerauthorization'}
                
    def clean(self):
        cleaned_data = self.cleaned_data
        try:
            email_is_valid=validate_email(cleaned_data['registeremail'])
        except:
            pass
        try:
            userExists=User._default_manager.get(username__iexact=cleaned_data['registerusername'])
            email_is_valid=validate_email(cleaned_data['registeremail'])
        except forms.ValidationError:
            raise forms.ValidationError("the email is in an invalid format")
        except:
            return cleaned_data
        raise forms.ValidationError("That e-mail address is already registered in our software.")

    def clean_registeremail(self):
        email = self.cleaned_data['registeremail']
        #inquire about regex validation from Egor
        email_is_valid=None
        try:
            email=User.objects.get(email=email.lower())
            raise forms.ValidationError('That username is already registered in our software.')
        except:
            pass
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            allUsernames=User._default_manager.get(username__iexact=cleaned_data['registerusername'])
        except User.DoesNotExist:
            return username
        except IntegrityError as e:
            raise forms.ValidationError("Username taken")
        if allUsernames is not None:
            raise forms.ValidationError("Username taken.")
        return username

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['registeremail']
        temp = self.cleaned_data['registeremail']
        user.username = self.cleaned_data['registerusername']

        if commit:
            #send_mail("welcome","eggie","info@app.eggie.co",[temp],fail_silently=False)
            #job = group([send_email.s(str(self),temp)])
            
            #job.apply_async()
            phone = self.cleaned_data['phone']
            sellerid = self.cleaned_data['registerseller_id']
            authkey = self.cleaned_data['registerauthorization']
            user.set_password(self.cleaned_data['registerpassword1'])
            user.save()
            client=models.Client(phone_number = phone, user_id = user.id)
            client.user = user
            client.client_id = user.id
            client.authorization = authkey
            client.seller_id = sellerid
            client.save()

        return user

class DocumentForm(forms.ModelForm):
    description = forms.CharField(required=False,max_length=128)
    myFile = forms.FileField()
    
    class Meta:
        model = Document
        fields = ('description','myFile')

    def save(self, username, document, commit=True):
        file = super(DocumentForm, self).save(commit=False)
        
        if commit:
            uuid_upload=str(uuid.uuid4())
            description = self.cleaned_data['description']
            fileread=self.cleaned_data['myFile']
            if description =='':
                description=uuid_upload
            user_id = User.objects.get(username=username).id
            document.name=uuid_upload+document.name
            file = Document(description = description, document = document,
                        client_id=user_id)
            file.save()
            
            job = group([file_upload.s(str(self),document.name, username,str(fileread),uuid_upload)])
            job.apply_async()
            
                #ftp.storbinary('STOR ' + str(outfile), open(outfile, 'rb'))
                
                
            #os.remove(str(file.document))
            # file.upload(DataFrame.to_dict(orient='records').update({'username':username}))
            return {
                "status":200,
                "file":file
            }
        else:
            return {
                "status":401,
                "file":None
            }
            
class ProductForm(forms.ModelForm):
    pro=Product.objects.all().values_list('title',flat=True)
    a=()
    for f in pro:
        a = list(a)
        a.append((f,f))
        a = tuple(a)
    product = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        required=False,
        choices=(
            a  )
        )
    product_min=forms.FloatField(label='product_min')
    product_max=forms.FloatField(label='product_max')
    
    class Meta:
        model = Product
        fields = ()
    
    def save(self,username,prod_new_min, prod_new_max, commit=True): #cid is client id.
        prod = super(ProductForm,self).save(commit=False) #finish this method
        
        if commit:
            cid=User.objects.get(username=username).id
            
            own_products = Product.objects.filter(client_id=cid)
            tracklist=self.cleaned_data['product']
            product_min=self.cleaned_data['product_min']
            
            
            for prod_min_keys,prod_min_values,prod_max_values in zip(prod_new_min.keys(),prod_new_min.values(),prod_new_max.values()):
                getProd=Product.objects.get(client_id=cid,title=prod_min_keys)
                
                if prod_min_values<=prod_max_values:
                    getProd.price_min=prod_min_values
                    getProd.price_max=prod_max_values
                
                #stored procedure will be needed soon
                getProd.save()
            
            for prod in own_products:
                if prod.title in tracklist:
                    prod.is_active=True
                else:
                    prod.is_active=False
                prod.save()
            
            #tracklist=self.cleaned_data()