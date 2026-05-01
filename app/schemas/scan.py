from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from enum import Enum


class SeverityLevel(str, Enum):
    """Severity levels for issues"""
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class IssueCategory(str, Enum):
    """Categories of issues"""
    SECURITY = "Security"
    PERFORMANCE = "Performance"
    CODE_STYLE = "Code Style"
    MAINTAINABILITY = "Maintainability"


class IssueDetail(BaseModel):
    """Detailed information about a specific issue"""
    
    severity: SeverityLevel = Field(..., description="Severity level of the issue")
    category: IssueCategory = Field(..., description="Category of the issue")
    title: str = Field(..., description="Title of the issue")
    description: str = Field(..., description="Detailed description of the issue")
    file: str = Field(..., description="File path where issue was found")
    line: int = Field(..., description="Line number where issue was found")
    recommendation: str = Field(..., description="Recommendation to fix the issue")
    
    class Config:
        json_schema_extra = {
            "example": {
                "severity": "High",
                "category": "Security",
                "title": "Hardcoded Credentials",
                "description": "Database credentials are hardcoded in the source code",
                "file": "app/core/database.py",
                "line": 15,
                "recommendation": "Use environment variables or secure vault for credentials"
            }
        }


class ScanRequest(BaseModel):
    """Schema for scan request payload"""
    
    url: Optional[str] = Field(None, description="URL to scan")
    platform: Optional[str] = Field(None, description="Social media platform")
    data: Optional[Dict[str, Any]] = Field(None, description="Additional data")
    
    class Config:
        json_schema_extra = {
            "example": {
                "url": "https://facebook.com/example",
                "platform": "facebook",
                "data": {"user_id": "123456"}
            }
        }


class ScanResponse(BaseModel):
    """Schema for scan response with detailed analysis results"""
    
    status: str = Field(default="success", description="Status of the scan operation")
    scanned_files: int = Field(..., description="Number of files scanned")
    issues_found: int = Field(..., description="Total number of issues found")
    details: List[IssueDetail] = Field(..., description="Detailed list of issues found")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "scanned_files": 142,
                "issues_found": 3,
                "details": [
                    {
                        "severity": "High",
                        "category": "Security",
                        "title": "Hardcoded Credentials",
                        "description": "Database credentials are hardcoded in the source code",
                        "file": "app/core/database.py",
                        "line": 15,
                        "recommendation": "Use environment variables or secure vault for credentials"
                    },
                    {
                        "severity": "Medium",
                        "category": "Performance",
                        "title": "N+1 Query Problem",
                        "description": "Multiple database queries in a loop causing performance issues",
                        "file": "app/services/user_service.py",
                        "line": 45,
                        "recommendation": "Use eager loading or batch queries to optimize database access"
                    },
                    {
                        "severity": "Low",
                        "category": "Code Style",
                        "title": "Missing Type Hints",
                        "description": "Function parameters lack type hints",
                        "file": "app/utils/helpers.py",
                        "line": 23,
                        "recommendation": "Add type hints to improve code readability and IDE support"
                    }
                ]
            }
        }

# Made with Bob
