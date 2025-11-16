import boto3
from botocore.config import Config
from app.config import settings
import uuid
from PIL import Image
import io

s3_client = boto3.client(
    's3',
    endpoint_url=settings.cloudflare_r2_endpoint,
    aws_access_key_id=settings.cloudflare_r2_access_key_id,
    aws_secret_access_key=settings.cloudflare_r2_secret_access_key,
    config=Config(signature_version='s3v4'),
    region_name='auto'
)

BUCKET_NAME = settings.cloudflare_r2_bucket_name


def optimize_image(image_data: bytes, max_width: int = 1920, quality: int = 85) -> bytes:
    """Optimize image for display"""
    img = Image.open(io.BytesIO(image_data))
    
    # Convert RGBA to RGB if needed
    if img.mode == 'RGBA':
        background = Image.new('RGB', img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[3])
        img = background
    elif img.mode != 'RGB':
        img = img.convert('RGB')
    
    # Resize if needed
    if img.width > max_width:
        ratio = max_width / img.width
        new_height = int(img.height * ratio)
        img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
    
    # Save as optimized JPEG
    output = io.BytesIO()
    img.save(output, format='JPEG', quality=quality, optimize=True)
    return output.getvalue()


def upload_image(full_image_data: bytes, user_id: int, post_id: int, image_num: int) -> tuple[str, str]:
    """Upload both full-res and display versions. Returns (display_url, full_url)"""
    file_ext = "jpg"
    full_filename = f"posts/{user_id}/{post_id}/full/image_{image_num}_{uuid.uuid4()}.{file_ext}"
    display_filename = f"posts/{user_id}/{post_id}/display/image_{image_num}_{uuid.uuid4()}.{file_ext}"
    
    # Optimize for display
    display_image_data = optimize_image(full_image_data)
    
    # Upload full resolution
    s3_client.put_object(
        Bucket=BUCKET_NAME,
        Key=full_filename,
        Body=full_image_data,
        ContentType='image/jpeg'
    )
    
    # Upload display version
    s3_client.put_object(
        Bucket=BUCKET_NAME,
        Key=display_filename,
        Body=display_image_data,
        ContentType='image/jpeg'
    )
    
    # Generate public URLs (adjust based on your R2 public URL format)
    # Assuming you have a public domain for your bucket
    base_url = f"https://pub-{settings.cloudflare_r2_bucket_name}.r2.dev"
    display_url = f"{base_url}/{display_filename}"
    full_url = f"{base_url}/{full_filename}"
    
    return display_url, full_url


def upload_avatar(image_data: bytes, user_id: int) -> str:
    """Upload user avatar"""
    # Optimize avatar (smaller size)
    img = Image.open(io.BytesIO(image_data))
    if img.mode == 'RGBA':
        background = Image.new('RGB', img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[3])
        img = background
    elif img.mode != 'RGB':
        img = img.convert('RGB')
    
    # Resize to max 400x400
    img.thumbnail((400, 400), Image.Resampling.LANCZOS)
    
    output = io.BytesIO()
    img.save(output, format='JPEG', quality=90, optimize=True)
    optimized_data = output.getvalue()
    
    filename = f"avatars/{user_id}/{uuid.uuid4()}.jpg"
    s3_client.put_object(
        Bucket=BUCKET_NAME,
        Key=filename,
        Body=optimized_data,
        ContentType='image/jpeg'
    )
    
    base_url = f"https://pub-{BUCKET_NAME}.r2.dev"
    return f"{base_url}/{filename}"


def get_signed_download_url(key: str, expires_in: int = 3600) -> str:
    """Generate signed URL for full-res download"""
    return s3_client.generate_presigned_url(
        'get_object',
        Params={'Bucket': BUCKET_NAME, 'Key': key},
        ExpiresIn=expires_in
    )
