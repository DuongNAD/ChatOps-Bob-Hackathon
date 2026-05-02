"""
Unit tests for the /scan endpoint

Test Coverage:
- Successful scan with valid request
- Scan with minimal/empty request
- Response structure validation
- Status code validation
- Response data types validation
- Issue details validation
- Edge cases and error scenarios
"""
import pytest
from fastapi import status
from app.schemas.scan import SeverityLevel, IssueCategory


class TestScanEndpoint:
    """Test suite for the /scan endpoint"""
    
    def test_scan_endpoint_success_with_full_request(self, test_client, sample_scan_request):
        """
        Test scan endpoint with complete request payload
        
        Validates:
        - HTTP 200 status code
        - Response contains all required fields
        - Response structure matches ScanResponse schema
        """
        response = test_client.post("/api/v1/scan", json=sample_scan_request)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        # Validate response structure
        assert "status" in data
        assert "scanned_files" in data
        assert "issues_found" in data
        assert "details" in data
        
        # Validate data types
        assert isinstance(data["status"], str)
        assert isinstance(data["scanned_files"], int)
        assert isinstance(data["issues_found"], int)
        assert isinstance(data["details"], list)
    
    def test_scan_endpoint_success_with_minimal_request(self, test_client, minimal_scan_request):
        """
        Test scan endpoint with minimal/empty request (all fields are optional)
        
        Validates:
        - Endpoint accepts empty request body
        - Returns valid response even with no input
        """
        response = test_client.post("/api/v1/scan", json=minimal_scan_request)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert data["status"] == "success"
        assert data["scanned_files"] > 0
        assert data["issues_found"] >= 0
    
    def test_scan_response_status_is_success(self, test_client, sample_scan_request):
        """
        Test that scan response status is 'success'
        """
        response = test_client.post("/api/v1/scan", json=sample_scan_request)
        data = response.json()
        
        assert data["status"] == "success"
    
    def test_scan_response_scanned_files_count(self, test_client, sample_scan_request):
        """
        Test that scanned_files count is a positive integer
        """
        response = test_client.post("/api/v1/scan", json=sample_scan_request)
        data = response.json()
        
        assert data["scanned_files"] == 142
        assert data["scanned_files"] > 0
        assert isinstance(data["scanned_files"], int)
    
    def test_scan_response_issues_found_matches_details_length(self, test_client, sample_scan_request):
        """
        Test that issues_found count matches the length of details array
        """
        response = test_client.post("/api/v1/scan", json=sample_scan_request)
        data = response.json()
        
        assert data["issues_found"] == len(data["details"])
    
    def test_scan_response_contains_three_sample_issues(self, test_client, sample_scan_request):
        """
        Test that response contains exactly 3 sample issues
        """
        response = test_client.post("/api/v1/scan", json=sample_scan_request)
        data = response.json()
        
        assert len(data["details"]) == 3
        assert data["issues_found"] == 3
    
    def test_scan_issue_details_structure(self, test_client, sample_scan_request):
        """
        Test that each issue in details has the correct structure
        
        Validates:
        - All required fields are present
        - Field types are correct
        """
        response = test_client.post("/api/v1/scan", json=sample_scan_request)
        data = response.json()
        
        for issue in data["details"]:
            # Check all required fields exist
            assert "severity" in issue
            assert "category" in issue
            assert "title" in issue
            assert "description" in issue
            assert "file" in issue
            assert "line" in issue
            assert "recommendation" in issue
            
            # Check field types
            assert isinstance(issue["severity"], str)
            assert isinstance(issue["category"], str)
            assert isinstance(issue["title"], str)
            assert isinstance(issue["description"], str)
            assert isinstance(issue["file"], str)
            assert isinstance(issue["line"], int)
            assert isinstance(issue["recommendation"], str)
    
    def test_scan_issue_severity_levels_are_valid(self, test_client, sample_scan_request):
        """
        Test that all severity levels are valid enum values
        """
        response = test_client.post("/api/v1/scan", json=sample_scan_request)
        data = response.json()
        
        valid_severities = [level.value for level in SeverityLevel]
        
        for issue in data["details"]:
            assert issue["severity"] in valid_severities
    
    def test_scan_issue_categories_are_valid(self, test_client, sample_scan_request):
        """
        Test that all issue categories are valid enum values
        """
        response = test_client.post("/api/v1/scan", json=sample_scan_request)
        data = response.json()
        
        valid_categories = [cat.value for cat in IssueCategory]
        
        for issue in data["details"]:
            assert issue["category"] in valid_categories
    
    def test_scan_issue_line_numbers_are_positive(self, test_client, sample_scan_request):
        """
        Test that all line numbers are positive integers
        """
        response = test_client.post("/api/v1/scan", json=sample_scan_request)
        data = response.json()
        
        for issue in data["details"]:
            assert issue["line"] > 0
            assert isinstance(issue["line"], int)
    
    def test_scan_first_issue_is_security_high(self, test_client, sample_scan_request):
        """
        Test that the first issue is a HIGH severity SECURITY issue
        """
        response = test_client.post("/api/v1/scan", json=sample_scan_request)
        data = response.json()
        
        first_issue = data["details"][0]
        assert first_issue["severity"] == SeverityLevel.HIGH.value
        assert first_issue["category"] == IssueCategory.SECURITY.value
        assert first_issue["title"] == "Hardcoded Credentials"
        assert first_issue["file"] == "app/core/database.py"
        assert first_issue["line"] == 15
    
    def test_scan_second_issue_is_performance_medium(self, test_client, sample_scan_request):
        """
        Test that the second issue is a MEDIUM severity PERFORMANCE issue
        """
        response = test_client.post("/api/v1/scan", json=sample_scan_request)
        data = response.json()
        
        second_issue = data["details"][1]
        assert second_issue["severity"] == SeverityLevel.MEDIUM.value
        assert second_issue["category"] == IssueCategory.PERFORMANCE.value
        assert second_issue["title"] == "N+1 Query Problem"
        assert second_issue["file"] == "app/services/user_service.py"
        assert second_issue["line"] == 45
    
    def test_scan_third_issue_is_code_style_low(self, test_client, sample_scan_request):
        """
        Test that the third issue is a LOW severity CODE_STYLE issue
        """
        response = test_client.post("/api/v1/scan", json=sample_scan_request)
        data = response.json()
        
        third_issue = data["details"][2]
        assert third_issue["severity"] == SeverityLevel.LOW.value
        assert third_issue["category"] == IssueCategory.CODE_STYLE.value
        assert third_issue["title"] == "Missing Type Hints"
        assert third_issue["file"] == "app/utils/helpers.py"
        assert third_issue["line"] == 23
    
    def test_scan_all_issues_have_non_empty_descriptions(self, test_client, sample_scan_request):
        """
        Test that all issues have non-empty descriptions
        """
        response = test_client.post("/api/v1/scan", json=sample_scan_request)
        data = response.json()
        
        for issue in data["details"]:
            assert len(issue["description"]) > 0
            assert issue["description"].strip() != ""
    
    def test_scan_all_issues_have_recommendations(self, test_client, sample_scan_request):
        """
        Test that all issues have non-empty recommendations
        """
        response = test_client.post("/api/v1/scan", json=sample_scan_request)
        data = response.json()
        
        for issue in data["details"]:
            assert len(issue["recommendation"]) > 0
            assert issue["recommendation"].strip() != ""
    
    def test_scan_endpoint_with_different_platforms(self, test_client):
        """
        Test scan endpoint with different platform values
        """
        platforms = ["facebook", "twitter", "instagram", "linkedin"]
        
        for platform in platforms:
            request_data = {
                "url": f"https://{platform}.com/example",
                "platform": platform,
                "data": {"user_id": "123"}
            }
            response = test_client.post("/api/v1/scan", json=request_data)
            
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert data["status"] == "success"
    
    def test_scan_endpoint_with_only_url(self, test_client):
        """
        Test scan endpoint with only URL provided
        """
        request_data = {"url": "https://example.com"}
        response = test_client.post("/api/v1/scan", json=request_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "success"
    
    def test_scan_endpoint_with_complex_data(self, test_client):
        """
        Test scan endpoint with complex nested data structure
        """
        request_data = {
            "url": "https://example.com",
            "platform": "custom",
            "data": {
                "user_id": "123",
                "metadata": {
                    "tags": ["security", "performance"],
                    "priority": "high"
                },
                "options": {
                    "deep_scan": True,
                    "max_depth": 5
                }
            }
        }
        response = test_client.post("/api/v1/scan", json=request_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "success"
    
    def test_scan_response_json_serializable(self, test_client, sample_scan_request):
        """
        Test that the response is properly JSON serializable
        """
        response = test_client.post("/api/v1/scan", json=sample_scan_request)
        
        # If we can get json(), it's properly serializable
        data = response.json()
        assert data is not None
        
        # Verify we can access nested data
        assert isinstance(data["details"], list)
        if len(data["details"]) > 0:
            assert isinstance(data["details"][0], dict)
    
    def test_scan_endpoint_content_type(self, test_client, sample_scan_request):
        """
        Test that response has correct content type
        """
        response = test_client.post("/api/v1/scan", json=sample_scan_request)
        
        assert "application/json" in response.headers["content-type"]
    
    @pytest.mark.asyncio
    async def test_scan_endpoint_is_async(self, test_client, sample_scan_request):
        """
        Test that the endpoint works with async operations
        """
        response = test_client.post("/api/v1/scan", json=sample_scan_request)
        
        assert response.status_code == status.HTTP_200_OK


class TestScanEndpointEdgeCases:
    """Test suite for edge cases and boundary conditions"""
    
    def test_scan_with_null_values(self, test_client):
        """
        Test scan endpoint with null values in optional fields
        """
        request_data = {
            "url": None,
            "platform": None,
            "data": None
        }
        response = test_client.post("/api/v1/scan", json=request_data)
        
        # Should still return 200 as all fields are optional
        assert response.status_code == status.HTTP_200_OK
    
    def test_scan_with_empty_strings(self, test_client):
        """
        Test scan endpoint with empty string values
        """
        request_data = {
            "url": "",
            "platform": "",
            "data": {}
        }
        response = test_client.post("/api/v1/scan", json=request_data)
        
        assert response.status_code == status.HTTP_200_OK
    
    def test_scan_with_very_long_url(self, test_client):
        """
        Test scan endpoint with very long URL
        """
        long_url = "https://example.com/" + "a" * 1000
        request_data = {"url": long_url}
        response = test_client.post("/api/v1/scan", json=request_data)
        
        assert response.status_code == status.HTTP_200_OK
    
    def test_scan_response_consistency(self, test_client, sample_scan_request):
        """
        Test that multiple calls return consistent results
        """
        response1 = test_client.post("/api/v1/scan", json=sample_scan_request)
        response2 = test_client.post("/api/v1/scan", json=sample_scan_request)
        
        data1 = response1.json()
        data2 = response2.json()
        
        # Results should be consistent
        assert data1["scanned_files"] == data2["scanned_files"]
        assert data1["issues_found"] == data2["issues_found"]
        assert len(data1["details"]) == len(data2["details"])


class TestScanEndpointPerformance:
    """Test suite for performance-related tests"""
    
    def test_scan_endpoint_response_time(self, test_client, sample_scan_request):
        """
        Test that scan endpoint responds in reasonable time
        Note: This is a basic check, not a comprehensive performance test
        """
        import time
        
        start_time = time.time()
        response = test_client.post("/api/v1/scan", json=sample_scan_request)
        end_time = time.time()
        
        response_time = end_time - start_time
        
        assert response.status_code == status.HTTP_200_OK
        # Response should be under 5 seconds (generous limit for unit test)
        assert response_time < 5.0
    
    def test_scan_multiple_concurrent_requests(self, test_client, sample_scan_request):
        """
        Test handling multiple requests (simulated concurrency)
        """
        responses = []
        for _ in range(5):
            response = test_client.post("/api/v1/scan", json=sample_scan_request)
            responses.append(response)
        
        # All requests should succeed
        for response in responses:
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert data["status"] == "success"

# Made with Bob
