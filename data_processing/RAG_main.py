import os
import boto3
from dotenv import load_dotenv
from logger_code import get_logger
from docling_markdown import convert_and_save_document
from pinecone_upsert import upsert_pinecone
from chunking_embedding import chunking_embedding_strategy

bucket_name = "bigdatasystems2"

# Create separate loggers for each ETL process
s3_files_logger = get_logger("s3_files", "s3_files.log")
docling_markdown_logger = get_logger("docling_markdown", "docling_markdown.log")
chunk_analyse_logger = get_logger("chunk_analyze", "chunk_analyze.log")
chunk_embed_logger = get_logger("chunk_embed", "chunk_embed.log")
pinecone_upsert_logger = get_logger("pinecone_upsert", "pinecone_upsert.log")

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

s3_files_logger.info("Pipeline execution started.")

for year in years:
    for quarter in quarters:

        filepath = f'NVIDIAFiles/{year}/NVIDIA_{year}_{quarter}.pdf'
        filename = f'NVIDIA_{year}_{quarter}.pdf'
        s3_files_logger.info(f'Fetching the file: {filename}')

        try:
            s3_client = get_s3_client()
            response = s3_client.get_object(Bucket=bucket_name, Key=filepath)
            file = response['Body'].read()

            s3_files_logger.info(f"Retrieved the file: {filename}")

        except Exception as e:
            s3_files_logger.error(f"Error retrieving file: {str(e)}")

        docling_markdown_logger.info(f'Starting markdown conversion for file: {filename}')
        markdown_file = convert_and_save_document(file)
        docling_markdown_logger.info(f'Markdown conversion finished for file: {filename}')

        chunk_embed_logger.info(f'Starting chunking and embedding for file: {filename}')
        embed_json = chunking_embedding_strategy(markdown_file, year, quarter)
        chunk_embed_logger.info(f'Finished chunking and embedding for file: {filename}')

        result = upsert_pinecone(embed_json, year, quarter)
        pinecone_upsert_logger.info(f'The chuncks are upserted to Pinecone along with its metadata. The statistics are: {result}')

s3_files_logger.info("Pipeline execution completed.")
    

