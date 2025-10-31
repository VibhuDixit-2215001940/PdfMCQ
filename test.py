import requests

url = "https://pdfmcq.onrender.com/extract"  # ✅ use correct route
files = {"file": open("MCQ_Test_Image_Based_With_Uploaded_Pics.pdf", "rb")}
res = requests.post(url, files=files)

print(res.status_code)
print(res.json())
