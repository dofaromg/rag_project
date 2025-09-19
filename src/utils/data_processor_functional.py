#!/usr/bin/env python3
"""
Refactored data_processor.py - Functional programming approach
This script demonstrates functional programming patterns for data processing.
"""

import json
import csv
import os
from datetime import datetime
from typing import List, Dict, Any, Callable, Optional, Union, Tuple
from functools import reduce, partial
from itertools import chain
import operator


# Pure functions for data validation
def is_valid_email(email: str) -> bool:
    """Pure function to validate email format"""
    return isinstance(email, str) and '@' in email and '.' in email.split('@')[-1]


def is_valid_age(age: Union[str, int, None]) -> bool:
    """Pure function to validate age"""
    try:
        age_int = int(age) if age is not None else 0
        return 0 <= age_int <= 150
    except (ValueError, TypeError):
        return False


def is_positive_number(value: Union[str, int, float, None]) -> bool:
    """Pure function to check if value is a positive number"""
    try:
        return float(value) >= 0 if value is not None else False
    except (ValueError, TypeError):
        return False


def is_future_date(date_obj: Optional[datetime]) -> bool:
    """Pure function to check if date is in the future"""
    return isinstance(date_obj, datetime) and date_obj > datetime.now()


# Pure functions for data transformation
def safe_int_convert(value: Any) -> Optional[int]:
    """Safely convert value to int"""
    try:
        return int(value) if value is not None else None
    except (ValueError, TypeError):
        return None


def safe_float_convert(value: Any) -> float:
    """Safely convert value to float"""
    try:
        return float(value) if value is not None else 0.0
    except (ValueError, TypeError):
        return 0.0


def safe_date_convert(value: str) -> Optional[datetime]:
    """Safely convert string to datetime"""
    if not isinstance(value, str):
        return None
    
    date_formats = ['%Y-%m-%d', '%Y-%m-%d %H:%M:%S']
    for fmt in date_formats:
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue
    return None


def normalize_string(value: Any) -> str:
    """Normalize string value"""
    return value.strip().title() if isinstance(value, str) else str(value)


# Higher-order functions for record processing
def create_validator(required_fields: List[str], 
                    type_validators: Dict[str, Callable]) -> Callable[[Dict], bool]:
    """Create a validator function for records"""
    def validate_record(record: Dict[str, Any]) -> bool:
        if not isinstance(record, dict):
            return False
        
        # Check required fields
        if not all(field in record and record[field] is not None 
                  for field in required_fields):
            return False
        
        # Apply type-specific validators
        record_type = record.get('type')
        if record_type in type_validators:
            return type_validators[record_type](record)
        
        return True
    
    return validate_record


def create_transformer(field_transformers: Dict[str, Callable]) -> Callable[[Dict], Dict]:
    """Create a transformer function for records"""
    def transform_record(record: Dict[str, Any]) -> Dict[str, Any]:
        return {
            key: field_transformers.get(key, lambda x: x)(value)
            for key, value in record.items()
        }
    
    return transform_record


def create_business_rule_filter(rules: List[Callable[[Dict], bool]]) -> Callable[[Dict], bool]:
    """Create a filter function based on business rules"""
    def apply_rules(record: Dict[str, Any]) -> bool:
        return all(rule(record) for rule in rules)
    
    return apply_rules


# Type-specific validators
def validate_user_record(record: Dict[str, Any]) -> bool:
    """Validate user-specific fields"""
    validators = [
        lambda r: is_valid_email(r.get('email', '')),
        lambda r: is_valid_age(r.get('age'))
    ]
    return all(validator(record) for validator in validators)


def validate_transaction_record(record: Dict[str, Any]) -> bool:
    """Validate transaction-specific fields"""
    return is_positive_number(record.get('amount'))


def validate_product_record(record: Dict[str, Any]) -> bool:
    """Validate product-specific fields"""
    validators = [
        lambda r: bool(r.get('name', '').strip()),
        lambda r: is_positive_number(r.get('price', 0))
    ]
    return all(validator(record) for validator in validators)


# Type-specific transformers
def transform_user_record(record: Dict[str, Any]) -> Dict[str, Any]:
    """Transform user record with functional approach"""
    transformations = {
        'name': normalize_string,
        'email': lambda x: x.lower() if isinstance(x, str) else x,
        'age': safe_int_convert
    }
    
    transformed = create_transformer(transformations)(record)
    
    # Add category based on age
    age = transformed.get('age')
    if age is not None:
        if age >= 18:
            transformed['category'] = 'adult'
        elif age >= 13:
            transformed['category'] = 'teen'
        else:
            transformed['category'] = 'child'
    else:
        transformed['category'] = 'unknown'
    
    return transformed


def transform_transaction_record(record: Dict[str, Any]) -> Dict[str, Any]:
    """Transform transaction record with functional approach"""
    transformed = record.copy()
    amount = safe_float_convert(record.get('amount', 0))
    
    # Determine priority
    if amount > 1000:
        transformed['priority'] = 'high'
    elif amount > 100:
        transformed['priority'] = 'medium'
    else:
        transformed['priority'] = 'low'
    
    # Calculate fee
    fee_rate = 0.02 if amount > 500 else 0.05
    transformed['fee'] = amount * fee_rate
    
    return transformed


def transform_product_record(record: Dict[str, Any]) -> Dict[str, Any]:
    """Transform product record with functional approach"""
    transformed = record.copy()
    
    if 'name' in transformed:
        transformed['name'] = normalize_string(transformed['name'])
    
    price = safe_float_convert(record.get('price', 0))
    if price > 100:
        transformed['price_category'] = 'expensive'
    elif price > 20:
        transformed['price_category'] = 'moderate'
    else:
        transformed['price_category'] = 'cheap'
    
    return transformed


def transform_generic_record(record: Dict[str, Any]) -> Dict[str, Any]:
    """Transform generic record"""
    transformed = record.copy()
    transformed['processed_at'] = datetime.now().isoformat()
    return transformed


# Business rules as pure functions
def no_negative_amounts(record: Dict[str, Any]) -> bool:
    """Business rule: no negative amounts"""
    amount = record.get('amount')
    return amount is None or safe_float_convert(amount) >= 0


def no_future_dates(record: Dict[str, Any]) -> bool:
    """Business rule: no future dates"""
    date_fields = ['date', 'created_at', 'updated_at']
    return not any(is_future_date(record.get(field)) for field in date_fields)


def valid_email_format(record: Dict[str, Any]) -> bool:
    """Business rule: valid email format"""
    email = record.get('email')
    return email is None or is_valid_email(str(email))


# File processing functions
def read_json_file(file_path: str) -> List[Dict[str, Any]]:
    """Pure function to read JSON file"""
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        return data if isinstance(data, list) else [data]
    except Exception:
        return []


def read_csv_file(file_path: str) -> List[Dict[str, Any]]:
    """Pure function to read CSV file"""
    try:
        with open(file_path, 'r') as f:
            return list(csv.DictReader(f))
    except Exception:
        return []


def process_csv_row(row: Dict[str, Any]) -> Dict[str, Any]:
    """Process a single CSV row with functional transformations"""
    field_processors = {
        'id': safe_int_convert,
        'user_id': safe_int_convert,
        'product_id': safe_int_convert,
        'price': safe_float_convert,
        'amount': safe_float_convert,
        'total': safe_float_convert,
        'date': safe_date_convert,
        'created_at': safe_date_convert,
        'updated_at': safe_date_convert
    }
    
    processed = {}
    for key, value in row.items():
        processor = field_processors.get(key.lower(), 
                                       lambda x: x.strip() if isinstance(x, str) else x)
        processed[key] = processor(value)
    
    return processed


# Main processing pipeline functions
def create_file_processor(file_readers: Dict[str, Callable]) -> Callable[[str], List[Dict]]:
    """Create a file processor based on file extension"""
    def process_file(file_path: str) -> List[Dict[str, Any]]:
        if not os.path.exists(file_path):
            return []
        
        extension = file_path.split('.')[-1].lower()
        reader = file_readers.get(extension, lambda _: [])
        return reader(file_path)
    
    return process_file


def create_record_processor(validators: Dict[str, Callable],
                          transformers: Dict[str, Callable],
                          business_rules: List[Callable]) -> Callable[[Dict], Optional[Dict]]:
    """Create a record processor pipeline"""
    def process_record(record: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        # Validation pipeline
        record_type = record.get('type', 'generic')
        validator = validators.get(record_type, lambda _: True)
        
        if not validator(record):
            return None
        
        # Transformation pipeline
        transformer = transformers.get(record_type, transform_generic_record)
        transformed = transformer(record)
        
        # Business rules pipeline
        rule_filter = create_business_rule_filter(business_rules)
        if not rule_filter(transformed):
            return None
        
        return transformed
    
    return process_record


def remove_duplicates_by_id(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Remove duplicates based on ID using functional approach"""
    seen_ids = set()
    unique_records = []
    
    for record in records:
        record_id = record.get('id')
        if record_id is None or record_id not in seen_ids:
            if record_id is not None:
                seen_ids.add(record_id)
            unique_records.append(record)
    
    return unique_records


def sort_by_id(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Sort records by ID"""
    return sorted(records, key=lambda x: x.get('id', 0))


class FunctionalDataProcessor:
    """Functional data processor using composition and pure functions"""
    
    def __init__(self):
        # Configure file readers
        self.file_readers = {
            'json': read_json_file,
            'csv': lambda path: list(map(process_csv_row, read_csv_file(path)))
        }
        
        # Configure validators
        self.validators = {
            'user': validate_user_record,
            'transaction': validate_transaction_record,
            'product': validate_product_record
        }
        
        # Configure transformers
        self.transformers = {
            'user': transform_user_record,
            'transaction': transform_transaction_record,
            'product': transform_product_record
        }
        
        # Configure business rules
        self.business_rules = [
            no_negative_amounts,
            no_future_dates,
            valid_email_format
        ]
        
        # Create processing functions
        self.file_processor = create_file_processor(self.file_readers)
        self.record_processor = create_record_processor(
            self.validators, self.transformers, self.business_rules
        )
    
    def process_data_files(self, file_paths: List[str]) -> Dict[str, Any]:
        """Process multiple data files using functional composition"""
        start_time = datetime.now()
        
        # File processing pipeline
        all_records = list(chain.from_iterable(
            map(self.file_processor, file_paths)
        ))
        
        # Record processing pipeline
        processed_records = list(filter(
            lambda x: x is not None,
            map(self.record_processor, all_records)
        ))
        
        # Post-processing pipeline
        final_records = sort_by_id(remove_duplicates_by_id(processed_records))
        
        # Calculate statistics
        end_time = datetime.now()
        stats = {
            'total_records': len(all_records),
            'valid_records': len(final_records),
            'invalid_records': len(all_records) - len(final_records),
            'processing_time': (end_time - start_time).total_seconds()
        }
        
        # Collect errors (simplified for functional approach)
        errors = [f"File not found: {path}" for path in file_paths 
                 if not os.path.exists(path)]
        
        return {
            'processed_data': final_records,
            'stats': stats,
            'errors': errors
        }


# Utility functions for functional composition
def compose(*functions):
    """Compose multiple functions into a single function"""
    return reduce(lambda f, g: lambda x: f(g(x)), functions, lambda x: x)


def pipe(value, *functions):
    """Apply functions in sequence to a value"""
    return reduce(lambda acc, func: func(acc), functions, value)


def curry(func):
    """Convert a function to a curried version"""
    def curried(*args, **kwargs):
        if len(args) + len(kwargs) >= func.__code__.co_argcount:
            return func(*args, **kwargs)
        return partial(func, *args, **kwargs)
    return curried


def main():
    """Main function demonstrating functional approach"""
    processor = FunctionalDataProcessor()
    
    # Example usage with functional composition
    sample_files = ['data1.json', 'data2.csv', 'data3.json']
    
    # Process files using the functional pipeline
    result = processor.process_data_files(sample_files)
    
    # Display results using functional approach
    stats_formatter = lambda stats: f"""
Processing completed:
Total records: {stats['total_records']}
Valid records: {stats['valid_records']}
Invalid records: {stats['invalid_records']}
Processing time: {stats['processing_time']:.2f} seconds
"""
    
    print(stats_formatter(result['stats']))
    
    if result['errors']:
        error_formatter = lambda errors: '\n'.join(f"  - {error}" for error in errors)
        print(f"Errors encountered: {len(result['errors'])}")
        print(error_formatter(result['errors']))


if __name__ == "__main__":
    main()