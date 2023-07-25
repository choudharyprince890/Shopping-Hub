
# instal this before uploading data
# pip install --upgrade huggingface_hub

from datasets import load_dataset

dataset = load_dataset("image_folder", data_dir="/F/data_uploader_huggingface/dataset_folder")

dataset.push_to_gub("choudharyprince890/martin_valen_hoodies")