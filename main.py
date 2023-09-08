import cv2
import pdf2image
import PyPDF2
from pypdf import PdfMerger
import glob
import shutil, os
import easyocr , pytesseract
import csv



pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-ocr\\tesseract.exe"


def get_all_cropped_data(pdf_file,write_fields,count,pdf,img_no):

    # List no:
    reader = easyocr.Reader(['hi'])
    crop_list_part_no=pdf_file[0:100,1200:1550]
    List_part_no=(reader.readtext(crop_list_part_no,detail=0))

    crop_division_no_and_name=pdf_file[55:110,50:590]
    division_no=(reader.readtext(crop_division_no_and_name,detail=0))

    crop_age_as_on=pdf_file[2260:2330,10:300]
    age_as_on=(reader.readtext(crop_age_as_on,detail=0))

    crop_data_of_publication = pdf_file[2260:2330,600:1000]
    data_of_publication=(reader.readtext(crop_data_of_publication,detail=0))
    
    

    def get_row_datas(row_no):
 
    # croping single data from three datas
        crop_data_row1=row_no
        sub_crop_on_row1_0=crop_data_row1[0:205,10:510]
        sub_crop_on_row1_1=crop_data_row1[0:205,515:1020]
        sub_crop_on_row1_2=crop_data_row1[0:205,1020:]
        def sub_details(ref_img):
            crop_Name=ref_img[0:37,52:]
            Name=(pytesseract.image_to_string(crop_Name,lang="hin")).replace("\n", "").replace("|","").replace(": [","").replace(".","").replace(";","")
            crop_Other_name=ref_img[35:65,0:]
            Other_name=(pytesseract.image_to_string(crop_Other_name,lang="hin")).replace("\n", "").replace("|","").replace("'","")
            crop_house_no=ref_img[65:95,110:]
            house_no=(pytesseract.image_to_string(crop_house_no,lang="hin")).replace("\n", "")
            crop_age=ref_img[97:130,45:90]

            a=(reader.readtext(crop_age,detail=0))
        
            try:
                age=int(a[0])
            except:
                age=a


            crop_gender=ref_img[97:130,140:]
            gender=(pytesseract.image_to_string(crop_gender,lang="hin")).replace("\n", "").replace(":","")

            data=[Name,Other_name,house_no,age,gender]
            return  data

        
        sub_crop_row1_voter1=(pytesseract.image_to_string(sub_crop_on_row1_0[6:50,300:500])).replace("\n", "").replace("—_—___","")
        # croping reamining details
        sub_crop_row1_details1=sub_crop_on_row1_0[30:,0:370]
        sub_details1_data=sub_details(sub_crop_row1_details1)
        # sub_voterId_s_no1=(pytesseract.image_to_string(sub_crop_on_row1_0[0:35,10:120])).replace("\n", "")
        

        sub_crop_row1_voter2=(pytesseract.image_to_string(sub_crop_on_row1_1[6:50,300:500])).replace("\n", "").replace("—_—___","")
        
        # croping reamining details
        sub_crop_row1_details2=sub_crop_on_row1_1[30:,0:370]
        sub_details2_data=sub_details(sub_crop_row1_details2)
        # sub_voterId_s_no2=(pytesseract.image_to_string(sub_crop_on_row1_1[0:35,10:120])).replace("\n", "")
        


        sub_crop_row1_voter3=(pytesseract.image_to_string(sub_crop_on_row1_2[6:50,300:500])).replace("\n", "").replace("—_—___","").replace("—_____","")
        # croping reamining details
        sub_crop_row1_details3=sub_crop_on_row1_2[30:,0:370]
        sub_details3_data=sub_details(sub_crop_row1_details3)
        # sub_voterId_s_no3=(pytesseract.image_to_string(sub_crop_on_row1_2[0:35,10:120])).replace("\n", "")
        


        

        row_data=[[sub_crop_row1_voter1,sub_details1_data],[sub_crop_row1_voter2,sub_details2_data],[sub_crop_row1_voter3,sub_details3_data]]

        return row_data
    
    crop_data_row1=get_row_datas(pdf_file[110:315,55:])
    crop_data_row2=get_row_datas(pdf_file[313:510,55:])
    crop_data_row3=get_row_datas(pdf_file[510:710,55:])
    crop_data_row4=get_row_datas(pdf_file[710:910,55:])
    crop_data_row5=get_row_datas(pdf_file[910:1110,55:])
    crop_data_row6=get_row_datas(pdf_file[1110:1310,55:])
    crop_data_row7=get_row_datas(pdf_file[1310:1510,55:])
    crop_data_row8=get_row_datas(pdf_file[1510:1710,55:])
    crop_data_row9=get_row_datas(pdf_file[1710:1910,55:])
    crop_data_row10=get_row_datas(pdf_file[1905:2105,55:])

    # print(crop_data_row1)
    # print()
    # print(crop_data_row2)
    all_crop_data=[crop_data_row1,crop_data_row2,crop_data_row3,crop_data_row4,crop_data_row5,crop_data_row6,crop_data_row7,crop_data_row8,crop_data_row9,crop_data_row10]

    for y in all_crop_data:
        # print(x)
        for x in y:
            print(f"0{x}0")
            print()
            print(division_no)
            print(List_part_no)

            try:
                voter_id="".join(str(x[0]).split(" "))
            except:
                voter_id=x[0]
           
            try:
                Name=x[1][0]
            except:
                Name="none"

            try:
                #  पतीचे नाव  :  काशिराम वायगंणकर
                other_name=str(str(x[1][1]).split("|")[1]).split(":")[0]
                print("other_name : ",other_name)
                other_name_val=str(str(x[1][1]).split("|")[1]).split(":")[1]
            except:
                other_name=str(x[1][1]).split(" :")[0]
                try:
                    other_name_val=str(x[1][1]).split(" :")[1]
                except:
                    other_name_val=x[1][1]
            
            try:
                temp=other_name.split(":")[0].replace(" ","")
                print(f":{temp}:")
            except:
                print("tempppppp error")

            if (other_name=="पतीचे नाव") or (temp=="पतीचेनाव") :
                print("hello")
                husband_name=other_name_val
                father_name="-"
                spouse_name="-"
                mother_name="-"
                others="-"
            elif other_name=="वडीलांचे नाव" or temp=="वडीलांचेनाव":
                father_name=other_name_val
                husband_name="-"
                spouse_name="-"
                mother_name="-"
                others="-"
            elif other_name=="जोडीदाराचे नाव" or temp=="जोडीदाराचेनाव":
                spouse_name=other_name_val
                husband_name="-"
                father_name="-"
                mother_name="-"
                others="-"
            elif other_name=="आईचे नाव" or temp=="आईचेनाव":
                mother_name=other_name_val
                husband_name="-"
                father_name="-"
                spouse_name="-"
                others="-"
            else:
                husband_name="-"
                father_name="-"
                spouse_name="-"
                mother_name="-"
                others=f"{other_name} : {other_name_val}"

            house_no=x[1][2]
            age=x[1][3]
            gender=x[1][4]
            # print({
            #     "name": Name,
            #     "voter_id":voter_id,
            #     "husband_name":husband_name,
            #     "father_name":father_name,
            #     "spouse_name":spouse_name,
            #     "mother_name":mother_name,
            #     "others":others,
            #     "age":age,
            #     "house no":house_no,
            #     "gender":gender

            #        })
            # print()
            # print()

            # try:
            if x!=['', ['', '', '', [], ''], '']:
                write_fields.writerow([count,List_part_no[1],"Sindhudurg","269-kudal",division_no[1],voter_id,Name,husband_name,spouse_name,father_name,mother_name,others,house_no,age,gender,age_as_on[0],data_of_publication[0]])
                count=count+1
            # except:
                
            #     # write_fields.writerow(["failed"])
            #     error_fields.writerow([List_part_no,"269-kudal",pdf,img_no])
            #     count=count+1
    return count


pdfs = [x for x in glob.glob("data_pdfs/*")]
count=0
pdf_count=1
for pdf in pdfs:
    if pdf_count==3:
        print("Loop Breaked")
        break
    try:
        delete_dir=shutil.rmtree("data1")
        create_dir=os.makedirs("data1")
    except:
        create_dir=os.makedirs("data1")

    # read every pages 
    pfd_main_file=PyPDF2.PdfReader(pdf)
    total_pages=len(pfd_main_file.pages)
    print(total_pages)

    # converting all pdfpages to images
    file=pdf2image.convert_from_path(pdf,poppler_path=r"C:\Users\navin\Downloads\Release-23.08.0-0\poppler-23.08.0\Library\bin")
    for i in range(total_pages):
        print("i : ",i)
        # file=pdf2image.
        file[i].save(f"data1/new_img{i}.jpg","JPEG")

    # extract data from all images

    fields=["s.no","List part No","State District","Assembly","Division no & name","Voter id","Name","Husband name","spouse name","Father name","Mother name","other name","House no","Age","gender","age as on","Data of Publication"]
    csv_file=open("voter_data.csv","a",encoding='utf-8')
    write_fields=csv.writer(csv_file)
    write_fields.writerow(fields)
    error_file=open("error_data.csv","a",encoding='utf-8')
    error_fields=csv.writer(error_file)
    error_fields.writerow(["List_no","assembly","pdf_file_loop_no","images_loop_no"])

    for x in range(total_pages-1):
        print("Loop : ",x)
        img_no=x
        data_pdf = cv2.imread(f"data1/new_img{x}.jpg")
        counreturn=get_all_cropped_data(data_pdf,write_fields,count,pdf,img_no)
        count=counreturn
    
    count=count+1

    pdf_count=pdf_count+1

    
    
    














