from selenium import webdriver
import requests
import io
from selenium.webdriver.common.by import By
from PIL import Image
import time
import os

PATH = "C:\\Users\\wwwva\\Car classifier\\Dataset\\chromedriver.exe"

wd = webdriver.Chrome(PATH)

# car_name = "PUNCH"
# Brand = "TATA"
# sub_path = Brand + "_" + car_name
# print(os.chdir("C:\\Users\\wwwva\\Car classifier\\Dataset"))
# try:
#     os.mkdir(sub_path)
# except:
#     print("Directory exist")
#
# download_path = "C:\\Users\\wwwva\\Car classifier\\Dataset\\" + sub_path + "\\"
image_count = 200
delay_count = 2
main_class = "Q4LuWd"
sub_class = "n3VNCb"


def url_finder(car_name):
    views = ["front view", "side view", "back view"]

    urls = set()

    for view in views:
        wd.get("https://www.google.com/imghp?hl=en")
        search_box = wd.find_element("name", "q")
        search_box.send_keys(car_name + " car " + view)
        search_box.submit()
        url = (wd.current_url)
        urls.add(url)
    return urls


def download_image(download_path, url, file_name):
    try:
        image_content = requests.get(url).content
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file)
        file_path = download_path + file_name

        with open(file_path, "wb") as f:
            image.save(f, "JPEG")
        print("Success")


    except Exception as e:
        print('failed', e)


def get_images_from_google(wd, delay, max_images, url):
    def scroll_down(wd):
        time.sleep(4)
        wd.execute_script("window.scrollBy(0,350)", "")

    wd.get(url)

    image_urls = set()
    step = 0

    while len(image_urls) < image_count:
        scroll_down(wd)
        thumbnails = wd.find_elements(By.CLASS_NAME, main_class)

        for img in thumbnails[len(image_urls):max_images]:
            try:
                img.click()
                time.sleep(delay)
            except:
                continue

            images = wd.find_elements(By.CLASS_NAME, sub_class)

            for image in images:
                image_urls.add(image.get_attribute('src'))
                print(f"Found{len(image_urls)}")

    return image_urls


def main(car_name, Brand):
    i = 0

    sub_path = Brand + "_" + car_name

    print(os.chdir("C:\\Users\\wwwva\\Car classifier\\Dataset"))

    try:
        os.mkdir(sub_path)
    except:
        print("Directory exist")

    download_path = "C:\\Users\\wwwva\\Car classifier\\Dataset\\" + sub_path + "\\"

    url_main = url_finder(car_name)

    for url_sub in url_main:
        urls = get_images_from_google(wd, delay_count, image_count, url_sub)

        for url in urls:
            print(i)
            i += 1
            download_image(download_path, url, str(i) + ".jpg")


# Cars that are already scrapped
used_list = [["HYUNDAI", "VERNA"], ["MAHINDRA", "THAR"], ["MARUTI", "BREZZA"], ["TOYOTA", "FORTUNER"],
             ["MAHINDRA", "XUV700"], ["HYUNDAI", "CRETA"], ["MAHINDRA", "BOLERO"], ["MARUTI", "SWIFT"],
             ["MARUTI", "DZIRE"], ["TATA", "HARRIER"], ["MARUTI", "ERTIGA"], ["KIA", "SELTOS"] ]

main_list = [ ["HYUNDAI", "VENUE"]]

for brand, car_name in main_list:
    main(car_name, brand)

wd.quit()
