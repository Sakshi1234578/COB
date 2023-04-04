from api.config.config import Configuration
from datetime import datetime


def validate_kyc_doc(file):
    file_extension = file.name.split('.')[-1]
    allowed_types = Configuration.get_Property("ALLOWED_FILE_TYPES")
    if file_extension not in allowed_types:
        return {'status': False, 'message': 'File type not allowed. Allowed file types are: ' + allowed_types}
    file_size = file.size / (1024 * 1024)
    max_file_size = Configuration.get_Property("MAX_FILE_SIZE")
    if file_size > int(max_file_size):
        return {'status': False, 'message': 'File size exceeds maximum limit of ' + max_file_size + 'MB'}
    return {'status': True, 'message': 'File validated successfully'}


def generate_doc_name(file):
    file_extension = file.name.split('.')[-1]
    file_name = file.name.replace('.' + file_extension, '')
    file_name = file_name.replace(' ', '_') + '_' + str(datetime.now().strftime("%Y%m%d%H%M%S")) + '.' + file_extension
    return file_name
