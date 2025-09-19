#!/usr/bin/env python3
"""
Original data_processor.py - Complex data processing script with nested loops and conditions
This script demonstrates typical imperative programming patterns that need refactoring.
"""

import json
import csv
import os
from datetime import datetime
from typing import List, Dict, Any


class DataProcessor:
    def __init__(self):
        self.processed_data = []
        self.error_log = []
        self.stats = {
            'total_records': 0,
            'valid_records': 0,
            'invalid_records': 0,
            'processing_time': 0
        }
    
    def process_data_files(self, file_paths: List[str]) -> Dict[str, Any]:
        """Process multiple data files with complex nested logic"""
        start_time = datetime.now()
        
        for file_path in file_paths:
            if not os.path.exists(file_path):
                self.error_log.append(f"File not found: {file_path}")
                continue
                
            file_extension = file_path.split('.')[-1].lower()
            
            if file_extension == 'json':
                # Complex JSON processing with nested loops
                try:
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        
                    if isinstance(data, list):
                        for item in data:
                            self.stats['total_records'] += 1
                            
                            # Complex validation logic
                            if self._validate_record(item):
                                # Nested processing based on record type
                                if 'type' in item:
                                    if item['type'] == 'user':
                                        processed_item = self._process_user_record(item)
                                    elif item['type'] == 'transaction':
                                        processed_item = self._process_transaction_record(item)
                                    elif item['type'] == 'product':
                                        processed_item = self._process_product_record(item)
                                    else:
                                        processed_item = self._process_generic_record(item)
                                else:
                                    processed_item = self._process_generic_record(item)
                                
                                if processed_item:
                                    self.processed_data.append(processed_item)
                                    self.stats['valid_records'] += 1
                                else:
                                    self.stats['invalid_records'] += 1
                            else:
                                self.stats['invalid_records'] += 1
                                
                except Exception as e:
                    self.error_log.append(f"Error processing {file_path}: {str(e)}")
                    
            elif file_extension == 'csv':
                # Complex CSV processing
                try:
                    with open(file_path, 'r') as f:
                        reader = csv.DictReader(f)
                        
                        for row in reader:
                            self.stats['total_records'] += 1
                            
                            # Complex row processing
                            processed_row = {}
                            for key, value in row.items():
                                # Complex data transformation logic
                                if key.lower() in ['id', 'user_id', 'product_id']:
                                    try:
                                        processed_row[key] = int(value)
                                    except ValueError:
                                        processed_row[key] = None
                                elif key.lower() in ['price', 'amount', 'total']:
                                    try:
                                        processed_row[key] = float(value)
                                    except ValueError:
                                        processed_row[key] = 0.0
                                elif key.lower() in ['date', 'created_at', 'updated_at']:
                                    try:
                                        processed_row[key] = datetime.strptime(value, '%Y-%m-%d')
                                    except ValueError:
                                        try:
                                            processed_row[key] = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
                                        except ValueError:
                                            processed_row[key] = None
                                else:
                                    processed_row[key] = value.strip() if isinstance(value, str) else value
                            
                            # Complex validation and filtering
                            if self._validate_csv_record(processed_row):
                                # Apply business rules
                                if self._apply_business_rules(processed_row):
                                    self.processed_data.append(processed_row)
                                    self.stats['valid_records'] += 1
                                else:
                                    self.stats['invalid_records'] += 1
                            else:
                                self.stats['invalid_records'] += 1
                                
                except Exception as e:
                    self.error_log.append(f"Error processing {file_path}: {str(e)}")
            else:
                self.error_log.append(f"Unsupported file format: {file_extension}")
        
        # Complex post-processing
        self._post_process_data()
        
        end_time = datetime.now()
        self.stats['processing_time'] = (end_time - start_time).total_seconds()
        
        return {
            'processed_data': self.processed_data,
            'stats': self.stats,
            'errors': self.error_log
        }
    
    def _validate_record(self, record: Dict[str, Any]) -> bool:
        """Complex validation logic with nested conditions"""
        if not isinstance(record, dict):
            return False
            
        # Required fields validation
        required_fields = ['id']
        for field in required_fields:
            if field not in record or record[field] is None:
                return False
        
        # Type-specific validation
        if 'type' in record:
            if record['type'] == 'user':
                if 'email' not in record or '@' not in str(record['email']):
                    return False
                if 'age' in record:
                    try:
                        age = int(record['age'])
                        if age < 0 or age > 150:
                            return False
                    except (ValueError, TypeError):
                        return False
            elif record['type'] == 'transaction':
                if 'amount' not in record:
                    return False
                try:
                    amount = float(record['amount'])
                    if amount < 0:
                        return False
                except (ValueError, TypeError):
                    return False
            elif record['type'] == 'product':
                if 'name' not in record or not record['name']:
                    return False
                if 'price' in record:
                    try:
                        price = float(record['price'])
                        if price < 0:
                            return False
                    except (ValueError, TypeError):
                        return False
        
        return True
    
    def _validate_csv_record(self, record: Dict[str, Any]) -> bool:
        """CSV-specific validation logic"""
        if not record:
            return False
            
        # Check for empty records
        non_empty_values = [v for v in record.values() if v is not None and str(v).strip()]
        if len(non_empty_values) == 0:
            return False
            
        return True
    
    def _apply_business_rules(self, record: Dict[str, Any]) -> bool:
        """Complex business rules application"""
        # Rule 1: Filter out records with negative amounts
        if 'amount' in record and record['amount'] is not None:
            if record['amount'] < 0:
                return False
        
        # Rule 2: Filter out future dates
        date_fields = ['date', 'created_at', 'updated_at']
        for field in date_fields:
            if field in record and record[field] is not None:
                if isinstance(record[field], datetime) and record[field] > datetime.now():
                    return False
        
        # Rule 3: Filter out invalid email formats
        if 'email' in record and record['email'] is not None:
            email = str(record['email'])
            if '@' not in email or '.' not in email.split('@')[-1]:
                return False
        
        return True
    
    def _process_user_record(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """Process user-specific records"""
        processed = record.copy()
        
        # Complex user processing logic
        if 'name' in processed:
            processed['name'] = processed['name'].title()
        
        if 'email' in processed:
            processed['email'] = processed['email'].lower()
        
        if 'age' in processed:
            try:
                age = int(processed['age'])
                if age >= 18:
                    processed['category'] = 'adult'
                elif age >= 13:
                    processed['category'] = 'teen'
                else:
                    processed['category'] = 'child'
            except (ValueError, TypeError):
                processed['category'] = 'unknown'
        
        return processed
    
    def _process_transaction_record(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """Process transaction-specific records"""
        processed = record.copy()
        
        # Complex transaction processing
        if 'amount' in processed:
            try:
                amount = float(processed['amount'])
                if amount > 1000:
                    processed['priority'] = 'high'
                elif amount > 100:
                    processed['priority'] = 'medium'
                else:
                    processed['priority'] = 'low'
                
                # Calculate fees
                if amount > 500:
                    processed['fee'] = amount * 0.02
                else:
                    processed['fee'] = amount * 0.05
                    
            except (ValueError, TypeError):
                processed['priority'] = 'unknown'
                processed['fee'] = 0
        
        return processed
    
    def _process_product_record(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """Process product-specific records"""
        processed = record.copy()
        
        # Complex product processing
        if 'name' in processed:
            processed['name'] = processed['name'].strip().title()
        
        if 'price' in processed:
            try:
                price = float(processed['price'])
                if price > 100:
                    processed['price_category'] = 'expensive'
                elif price > 20:
                    processed['price_category'] = 'moderate'
                else:
                    processed['price_category'] = 'cheap'
            except (ValueError, TypeError):
                processed['price_category'] = 'unknown'
        
        return processed
    
    def _process_generic_record(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """Process generic records"""
        processed = record.copy()
        processed['processed_at'] = datetime.now().isoformat()
        return processed
    
    def _post_process_data(self):
        """Complex post-processing logic"""
        # Sort data by ID if available
        try:
            self.processed_data.sort(key=lambda x: x.get('id', 0))
        except (TypeError, KeyError):
            pass
        
        # Remove duplicates based on ID
        seen_ids = set()
        unique_data = []
        for item in self.processed_data:
            item_id = item.get('id')
            if item_id is not None and item_id not in seen_ids:
                seen_ids.add(item_id)
                unique_data.append(item)
            elif item_id is None:
                unique_data.append(item)
        
        self.processed_data = unique_data
        
        # Update stats
        self.stats['valid_records'] = len(self.processed_data)


def main():
    """Main function to demonstrate usage"""
    processor = DataProcessor()
    
    # Example usage
    sample_files = ['data1.json', 'data2.csv', 'data3.json']
    result = processor.process_data_files(sample_files)
    
    print(f"Processing completed:")
    print(f"Total records: {result['stats']['total_records']}")
    print(f"Valid records: {result['stats']['valid_records']}")
    print(f"Invalid records: {result['stats']['invalid_records']}")
    print(f"Processing time: {result['stats']['processing_time']:.2f} seconds")
    
    if result['errors']:
        print(f"Errors encountered: {len(result['errors'])}")
        for error in result['errors']:
            print(f"  - {error}")


if __name__ == "__main__":
    main()