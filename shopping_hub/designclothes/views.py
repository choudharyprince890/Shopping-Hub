from django.shortcuts import render
import requests

import os
import io
from PIL import Image
import matplotlib.pyplot as plt

# https://huggingface.co/Ali-fb/sd_martin_valen-model-v1-2_400?text=hoodie

API_URL = "https://api-inference.huggingface.co/models/Ali-fb/sd_martin_valen-model-v1-2_400"
headers = {"Authorization": f"Bearer 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"}

# Create your views here.
def designclothes(request):
    if request.method == 'GET':
        return render(request, 'design_clothes.html')
    else:
        prompt=request.POST.get('prompt')
        prompt = prompt.strip()

        payload = {"inputs": prompt}
        response = requests.post(API_URL, headers=headers, json=payload)
        response_img = response.content

        without_spaces = prompt.replace(" ", "")
        
        image = Image.open(io.BytesIO(response_img))


        image.save(f"store/static/generated/{without_spaces}.jpg")
        image.seek(0)
        
        gen_svd_img = f"store/static/generated/{without_spaces}.jpg"
        print("this is saved image path",gen_svd_img)
        print(type(gen_svd_img))



        # Read the image using PIL
        # img = Image.open(gen_svd_img)
        # plt.imshow(img)
        # plt.axis('off')  
        # plt.show()
        # dict = {'img_hex':gen_svd_img}
        

        return render(request, 'design_clothes.html', {'img':gen_svd_img,'key':without_spaces})


        