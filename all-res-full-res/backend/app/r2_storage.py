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
    """Optimize image for display - skip optimization for RAW files"""
    # Check if it's a RAW file by extension (we'll pass filename separately if needed)
    # For now, try to open with PIL - if it fails, it's likely RAW, return original
    try:
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
    except Exception:
        # If PIL can't open it, it's likely RAW - return original for display too
        return image_data


def upload_image(full_image_data: bytes, user_id: int, post_id: int, image_num: int, original_filename: str = None) -> tuple[str, str]:
    """Upload both full-res and display versions. Returns (display_url, full_url)"""
    # Determine file extension from original filename or default to jpg
    if original_filename:
        file_ext = original_filename.split('.')[-1].lower()
        # Normalize common extensions
        if file_ext in ['jpeg', 'jpg']:
            file_ext = 'jpg'
        elif file_ext in ['tiff', 'tif']:
            file_ext = 'tiff'
    else:
        file_ext = "jpg"
    
    full_filename = f"posts/{user_id}/{post_id}/full/image_{image_num}_{uuid.uuid4()}.{file_ext}"
    display_filename = f"posts/{user_id}/{post_id}/display/image_{image_num}_{uuid.uuid4()}.{file_ext}"
    
    # Optimize for display (will return original if RAW)
    display_image_data = optimize_image(full_image_data)
    
    # Determine content type
    content_type_map = {
        'jpg': 'image/jpeg',
        'jpeg': 'image/jpeg',
        'png': 'image/png',
        'tiff': 'image/tiff',
        'tif': 'image/tiff',
        'cr2': 'image/x-canon-cr2',
        'nef': 'image/x-nikon-nef',
        'arw': 'image/x-sony-arw',
        'raf': 'image/x-fuji-raf',
        'orf': 'image/x-olympus-orf',
        'rw2': 'image/x-panasonic-rw2',
        'pef': 'image/x-pentax-pef',
        'srw': 'image/x-samsung-srw',
        'dng': 'image/x-adobe-dng'
    }
    content_type = content_type_map.get(file_ext, 'application/octet-stream')
    
    # Upload full resolution (original, no compression)
    s3_client.put_object(
        Bucket=BUCKET_NAME,
        Key=full_filename,
        Body=full_image_data,
        ContentType=content_type
    )
    
    # Upload display version
    s3_client.put_object(
        Bucket=BUCKET_NAME,
        Key=display_filename,
        Body=display_image_data,
        ContentType=content_type if display_image_data == full_image_data else 'image/jpeg'
    )
    
    # Generate public URLs (adjust based on your R2 public URL format)
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
