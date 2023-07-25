from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage

# importing Products from mdel  
from store.models.products import Products

# importing libraries
import numpy as np
from numpy.linalg import norm
import tensorflow 
import keras.utils as image
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from sklearn.neighbors import NearestNeighbors
from keras.layers import GlobalMaxPooling2D 
import pickle



# importiong models from artifacts folder
feature_list = np.array(pickle.load(open('artifacts/embedding.pkl','rb')))
filenames = pickle.load(open('artifacts/filenames.pkl','rb'))




# Create your views here.
def find_product(request):
    if request.method == 'GET':
        cart = request.session.get('cart')
        if not cart:
            request.session['cart'] = {}
        return render(request, 'find_products.html')
    
    else:
        f_image = request.FILES['f_image']
        # Save the file to ./uploads
        fs = FileSystemStorage()
        file_path = fs.save('uploads/'+f_image.name,f_image)

        # using ResNet50 state of th art model 
        model = ResNet50(weights='imagenet',include_top=False,input_shape=(224,224,3))
        model.trainable = False

        model = tensorflow.keras.Sequential([
            model,
            GlobalMaxPooling2D()
        ])

        # resizing the image
        img = image.load_img(file_path,target_size=(224,224))
        # converting image to array
        img_array = image.img_to_array(img)

        # converting the araay from 3-d to 4-d, beacause keras doesn't work on single image it works on batches of image
        expanded_img_array = np.expand_dims(img_array, axis=0)
        # preprocessing the input (zeroo centring, RGB - BGR)
        preprocessed_img = preprocess_input(expanded_img_array)
        # extract features from image 
        result = model.predict(preprocessed_img).flatten()
        # normalizing the features
        normalized_result = result / norm(result)

        # using nearest NearestNeighbors algoritham for finding the nearest features
        neighbors = NearestNeighbors(n_neighbors=6,algorithm='brute',metric='euclidean')
        neighbors.fit(feature_list)
        distances,indices = neighbors.kneighbors([normalized_result])
        
        kagglepath_numbers = []
        for file in indices[0][1:6]:
            kaggle_path = filenames[file]
            string = kaggle_path
            filename = string.split('/')[-1]
            kagglepath_numbers.append(filename)

        prod = Products.objects.filter(filename__in=kagglepath_numbers)

        product = request.POST.get('product')
        print("this is add to cartt product-->",product)

        return render(request, 'find_products.html', {"products":prod})
    





# from django.views import View
# class FindProduct(View):
#     def get(self, request):
#         return render(request, 'find_products.html')

