from io import BytesIO
import os
import boto3
from dotenv import load_dotenv
from docling_markdown import convert_and_save_document
from pinecone_upsert import upsert_pinecone
from chunking_embedding import chunking_embedding_strategy


bucket_name = "bigdatasystems2"

def get_s3_client():

    #load_dotenv()
    load_dotenv(r'C:\Users\Admin\Desktop\MS Data Architecture and Management\DAMG 7245 - Big Data Systems and Intelligence Analytics\Assignment 5 A\environment\access.env')

    #s3 = boto3.client('s3')
    s3 = boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_REGION')
    )

    return s3


years = ['2024', '2023', '2022', '2021', '2020']
quarters = ['1', '2', '3', '4']

for year in years:
    for quarter in quarters:

        filepath = f'NVIDIAFiles/{year}/NVIDIA_{year}_{quarter}.pdf'
        filename = f'NVIDIA_{year}_{quarter}.pdf'
        print(f'Fetching the file: {filename}')

        try:
            s3_client = get_s3_client()
            response = s3_client.get_object(Bucket=bucket_name, Key=filepath)
            file = response['Body'].read()

            print(f"Retrieved the file: {filename}")

        except Exception as e:
            print(f"Error retrieving file: {str(e)}")

        print(f'Starting markdown conversion for file: {filename}')
        markdown_file = convert_and_save_document(file)
        print(f'Markdown conversion finished for file: {filename}')

        print(f'Starting chunking and embedding for file: {filename}')
        embed_json = chunking_embedding_strategy(markdown_file, year, quarter)
        print(f'Finished chunking and embedding for file: {filename}')

        result = upsert_pinecone(embed_json, year, quarter)
        print('The chuncks are upserted to Pinecone along with its metadata. The statistics are:')
        print(result)

    

