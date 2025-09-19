#!/usr/bin/env python3
"""
Test suite for functional data processor
验证重构后的函数式编程代码的正确性和性能
"""

import unittest
import tempfile
import json
import csv
import os
from datetime import datetime, timedelta
from typing import Dict, Any, List

# Import the functional data processor
from data_processor_functional import (
    # Pure functions
    is_valid_email,
    is_valid_age,
    is_positive_number,
    is_future_date,
    safe_int_convert,
    safe_float_convert,
    safe_date_convert,
    normalize_string,
    
    # Validators
    validate_user_record,
    validate_transaction_record,
    validate_product_record,
    
    # Transformers
    transform_user_record,
    transform_transaction_record,
    transform_product_record,
    transform_generic_record,
    
    # Business rules
    no_negative_amounts,
    no_future_dates,
    valid_email_format,
    
    # File processors
    read_json_file,
    read_csv_file,
    process_csv_row,
    
    # Utility functions
    compose,
    pipe,
    curry,
    
    # Main processor
    FunctionalDataProcessor
)


class TestPureFunctions(unittest.TestCase):
    """测试纯函数的正确性"""
    
    def test_is_valid_email(self):
        """测试邮箱验证函数"""
        # Valid emails
        self.assertTrue(is_valid_email("test@example.com"))
        self.assertTrue(is_valid_email("user.name@domain.co.uk"))
        
        # Invalid emails
        self.assertFalse(is_valid_email("invalid-email"))
        self.assertFalse(is_valid_email("@domain.com"))
        self.assertFalse(is_valid_email("user@"))
        self.assertFalse(is_valid_email(""))
        self.assertFalse(is_valid_email(None))
    
    def test_is_valid_age(self):
        """测试年龄验证函数"""
        # Valid ages
        self.assertTrue(is_valid_age(25))
        self.assertTrue(is_valid_age("30"))
        self.assertTrue(is_valid_age(0))
        self.assertTrue(is_valid_age(150))
        
        # Invalid ages
        self.assertFalse(is_valid_age(-1))
        self.assertFalse(is_valid_age(151))
        self.assertFalse(is_valid_age("invalid"))
        self.assertFalse(is_valid_age(None))
    
    def test_is_positive_number(self):
        """测试正数验证函数"""
        # Valid positive numbers
        self.assertTrue(is_positive_number(10))
        self.assertTrue(is_positive_number(10.5))
        self.assertTrue(is_positive_number("15"))
        self.assertTrue(is_positive_number(0))
        
        # Invalid numbers
        self.assertFalse(is_positive_number(-1))
        self.assertFalse(is_positive_number("-5"))
        self.assertFalse(is_positive_number("invalid"))
        self.assertFalse(is_positive_number(None))
    
    def test_safe_conversions(self):
        """测试安全类型转换函数"""
        # Integer conversion
        self.assertEqual(safe_int_convert("123"), 123)
        self.assertEqual(safe_int_convert(456), 456)
        self.assertIsNone(safe_int_convert("invalid"))
        self.assertIsNone(safe_int_convert(None))
        
        # Float conversion
        self.assertEqual(safe_float_convert("123.45"), 123.45)
        self.assertEqual(safe_float_convert(678), 678.0)
        self.assertEqual(safe_float_convert("invalid"), 0.0)
        self.assertEqual(safe_float_convert(None), 0.0)
        
        # Date conversion
        self.assertIsInstance(safe_date_convert("2023-01-01"), datetime)
        self.assertIsInstance(safe_date_convert("2023-01-01 12:00:00"), datetime)
        self.assertIsNone(safe_date_convert("invalid-date"))
        self.assertIsNone(safe_date_convert(None))
    
    def test_normalize_string(self):
        """测试字符串标准化函数"""
        self.assertEqual(normalize_string("  hello world  "), "Hello World")
        self.assertEqual(normalize_string("UPPERCASE"), "Uppercase")
        self.assertEqual(normalize_string(123), "123")


class TestValidators(unittest.TestCase):
    """测试验证器函数"""
    
    def test_validate_user_record(self):
        """测试用户记录验证"""
        # Valid user record
        valid_user = {
            "id": 1,
            "email": "user@example.com",
            "age": 25
        }
        self.assertTrue(validate_user_record(valid_user))
        
        # Invalid user records
        invalid_email = {"id": 1, "email": "invalid-email", "age": 25}
        self.assertFalse(validate_user_record(invalid_email))
        
        invalid_age = {"id": 1, "email": "user@example.com", "age": -5}
        self.assertFalse(validate_user_record(invalid_age))
    
    def test_validate_transaction_record(self):
        """测试交易记录验证"""
        # Valid transaction
        valid_transaction = {"id": 1, "amount": 100.50}
        self.assertTrue(validate_transaction_record(valid_transaction))
        
        # Invalid transaction
        invalid_transaction = {"id": 1, "amount": -50}
        self.assertFalse(validate_transaction_record(invalid_transaction))
    
    def test_validate_product_record(self):
        """测试产品记录验证"""
        # Valid product
        valid_product = {"id": 1, "name": "Product Name", "price": 29.99}
        self.assertTrue(validate_product_record(valid_product))
        
        # Invalid product
        invalid_product = {"id": 1, "name": "", "price": -10}
        self.assertFalse(validate_product_record(invalid_product))


class TestTransformers(unittest.TestCase):
    """测试转换器函数"""
    
    def test_transform_user_record(self):
        """测试用户记录转换"""
        user_record = {
            "id": 1,
            "name": "  john doe  ",
            "email": "JOHN@EXAMPLE.COM",
            "age": "25"
        }
        
        transformed = transform_user_record(user_record)
        
        self.assertEqual(transformed["name"], "John Doe")
        self.assertEqual(transformed["email"], "john@example.com")
        self.assertEqual(transformed["age"], 25)
        self.assertEqual(transformed["category"], "adult")
    
    def test_transform_transaction_record(self):
        """测试交易记录转换"""
        transaction_record = {"id": 1, "amount": "1500.00"}
        
        transformed = transform_transaction_record(transaction_record)
        
        self.assertEqual(transformed["priority"], "high")
        self.assertEqual(transformed["fee"], 30.0)  # 1500 * 0.02
    
    def test_transform_product_record(self):
        """测试产品记录转换"""
        product_record = {"id": 1, "name": "  expensive item  ", "price": "150.00"}
        
        transformed = transform_product_record(product_record)
        
        self.assertEqual(transformed["name"], "Expensive Item")
        self.assertEqual(transformed["price_category"], "expensive")


class TestBusinessRules(unittest.TestCase):
    """测试业务规则函数"""
    
    def test_no_negative_amounts(self):
        """测试负金额规则"""
        positive_record = {"amount": 100}
        negative_record = {"amount": -50}
        no_amount_record = {"id": 1}
        
        self.assertTrue(no_negative_amounts(positive_record))
        self.assertFalse(no_negative_amounts(negative_record))
        self.assertTrue(no_negative_amounts(no_amount_record))
    
    def test_no_future_dates(self):
        """测试未来日期规则"""
        past_date = datetime.now() - timedelta(days=1)
        future_date = datetime.now() + timedelta(days=1)
        
        past_record = {"date": past_date}
        future_record = {"date": future_date}
        no_date_record = {"id": 1}
        
        self.assertTrue(no_future_dates(past_record))
        self.assertFalse(no_future_dates(future_record))
        self.assertTrue(no_future_dates(no_date_record))
    
    def test_valid_email_format(self):
        """测试邮箱格式规则"""
        valid_record = {"email": "user@example.com"}
        invalid_record = {"email": "invalid-email"}
        no_email_record = {"id": 1}
        
        self.assertTrue(valid_email_format(valid_record))
        self.assertFalse(valid_email_format(invalid_record))
        self.assertTrue(valid_email_format(no_email_record))


class TestFileProcessors(unittest.TestCase):
    """测试文件处理函数"""
    
    def setUp(self):
        """设置测试数据"""
        self.temp_dir = tempfile.mkdtemp()
        
        # Create test JSON file
        self.json_data = [
            {"id": 1, "type": "user", "name": "John", "email": "john@example.com"},
            {"id": 2, "type": "transaction", "amount": 100.50}
        ]
        self.json_file = os.path.join(self.temp_dir, "test.json")
        with open(self.json_file, 'w') as f:
            json.dump(self.json_data, f)
        
        # Create test CSV file
        self.csv_file = os.path.join(self.temp_dir, "test.csv")
        with open(self.csv_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["id", "name", "price"])
            writer.writerow(["1", "Product A", "29.99"])
            writer.writerow(["2", "Product B", "49.99"])
    
    def tearDown(self):
        """清理测试数据"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_read_json_file(self):
        """测试JSON文件读取"""
        data = read_json_file(self.json_file)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["id"], 1)
        
        # Test non-existent file
        empty_data = read_json_file("non_existent.json")
        self.assertEqual(empty_data, [])
    
    def test_read_csv_file(self):
        """测试CSV文件读取"""
        data = read_csv_file(self.csv_file)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["id"], "1")
        
        # Test non-existent file
        empty_data = read_csv_file("non_existent.csv")
        self.assertEqual(empty_data, [])
    
    def test_process_csv_row(self):
        """测试CSV行处理"""
        row = {"id": "123", "price": "29.99", "date": "2023-01-01", "name": "  Product  "}
        processed = process_csv_row(row)
        
        self.assertEqual(processed["id"], 123)
        self.assertEqual(processed["price"], 29.99)
        self.assertIsInstance(processed["date"], datetime)
        self.assertEqual(processed["name"], "Product")


class TestUtilityFunctions(unittest.TestCase):
    """测试工具函数"""
    
    def test_compose(self):
        """测试函数组合"""
        add_one = lambda x: x + 1
        multiply_two = lambda x: x * 2
        
        composed = compose(multiply_two, add_one)
        result = composed(5)  # (5 + 1) * 2 = 12
        self.assertEqual(result, 12)
    
    def test_pipe(self):
        """测试管道处理"""
        add_one = lambda x: x + 1
        multiply_two = lambda x: x * 2
        
        result = pipe(5, add_one, multiply_two)  # (5 + 1) * 2 = 12
        self.assertEqual(result, 12)
    
    def test_curry(self):
        """测试柯里化"""
        @curry
        def add_three_numbers(a, b, c):
            return a + b + c
        
        # Partial application
        add_five = add_three_numbers(2, 3)
        result = add_five(4)  # 2 + 3 + 4 = 9
        self.assertEqual(result, 9)


class TestFunctionalDataProcessor(unittest.TestCase):
    """测试主要的函数式数据处理器"""
    
    def setUp(self):
        """设置测试环境"""
        self.processor = FunctionalDataProcessor()
        self.temp_dir = tempfile.mkdtemp()
        
        # Create test files
        self.create_test_files()
    
    def tearDown(self):
        """清理测试环境"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def create_test_files(self):
        """创建测试文件"""
        # JSON file with mixed data
        json_data = [
            {"id": 1, "type": "user", "name": "John Doe", "email": "john@example.com", "age": 25},
            {"id": 2, "type": "transaction", "amount": 150.75},
            {"id": 3, "type": "product", "name": "Laptop", "price": 999.99},
            {"id": 4, "type": "user", "email": "invalid-email", "age": -5},  # Invalid
        ]
        
        self.json_file = os.path.join(self.temp_dir, "test_data.json")
        with open(self.json_file, 'w') as f:
            json.dump(json_data, f)
        
        # CSV file
        self.csv_file = os.path.join(self.temp_dir, "test_data.csv")
        with open(self.csv_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["id", "name", "price", "amount"])
            writer.writerow(["5", "Product A", "29.99", ""])
            writer.writerow(["6", "Product B", "49.99", "100"])
            writer.writerow(["7", "", "", "-50"])  # Invalid
    
    def test_process_data_files(self):
        """测试完整的数据处理流程"""
        file_paths = [self.json_file, self.csv_file]
        result = self.processor.process_data_files(file_paths)
        
        # Check structure
        self.assertIn('processed_data', result)
        self.assertIn('stats', result)
        self.assertIn('errors', result)
        
        # Check stats
        stats = result['stats']
        self.assertGreater(stats['total_records'], 0)
        self.assertGreater(stats['valid_records'], 0)
        self.assertGreaterEqual(stats['invalid_records'], 0)
        self.assertGreater(stats['processing_time'], 0)
        
        # Check that invalid records are filtered out
        processed_data = result['processed_data']
        for record in processed_data:
            # All processed records should have valid IDs
            self.assertIsNotNone(record.get('id'))
    
    def test_error_handling(self):
        """测试错误处理"""
        # Test with non-existent files
        file_paths = ["non_existent1.json", "non_existent2.csv"]
        result = self.processor.process_data_files(file_paths)
        
        # Should handle errors gracefully
        self.assertEqual(len(result['errors']), 2)
        self.assertEqual(result['stats']['total_records'], 0)
        self.assertEqual(result['stats']['valid_records'], 0)


class TestPerformance(unittest.TestCase):
    """性能测试"""
    
    def setUp(self):
        """设置性能测试环境"""
        self.processor = FunctionalDataProcessor()
        self.temp_dir = tempfile.mkdtemp()
        
        # Create large test file
        self.create_large_test_file()
    
    def tearDown(self):
        """清理测试环境"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def create_large_test_file(self):
        """创建大型测试文件"""
        large_data = []
        for i in range(1000):  # 1000 records
            large_data.append({
                "id": i,
                "type": "user" if i % 3 == 0 else "transaction",
                "name": f"User {i}",
                "email": f"user{i}@example.com",
                "age": 20 + (i % 50),
                "amount": 100 + (i % 1000)
            })
        
        self.large_file = os.path.join(self.temp_dir, "large_data.json")
        with open(self.large_file, 'w') as f:
            json.dump(large_data, f)
    
    def test_large_file_processing(self):
        """测试大文件处理性能"""
        start_time = datetime.now()
        
        result = self.processor.process_data_files([self.large_file])
        
        end_time = datetime.now()
        processing_time = (end_time - start_time).total_seconds()
        
        # Performance assertions
        self.assertLess(processing_time, 5.0)  # Should complete within 5 seconds
        self.assertEqual(result['stats']['total_records'], 1000)
        self.assertGreater(result['stats']['valid_records'], 900)  # Most should be valid


if __name__ == '__main__':
    # Run all tests
    unittest.main(verbosity=2)