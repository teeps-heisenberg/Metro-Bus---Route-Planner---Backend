#!/usr/bin/env python3
"""
Metro Bus Route Planner Backend - Updated Project Documentation Generator
Creates a comprehensive PDF documenting all technologies, processes, and team member responsibilities.
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import Image
import os
from datetime import datetime

def create_updated_project_documentation():
    """Create comprehensive project documentation PDF with team member responsibilities."""
    
    # Create PDF document
    doc = SimpleDocTemplate(
        "Metro_Bus_Route_Planner_Backend_Documentation_Updated.pdf",
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=18
    )
    
    # Get styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=colors.darkblue
    )
    
    heading1_style = ParagraphStyle(
        'CustomHeading1',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=12,
        spaceBefore=20,
        textColor=colors.darkblue
    )
    
    heading2_style = ParagraphStyle(
        'CustomHeading2',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=8,
        spaceBefore=12,
        textColor=colors.darkgreen
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=6,
        alignment=TA_JUSTIFY
    )
    
    code_style = ParagraphStyle(
        'CustomCode',
        parent=styles['Code'],
        fontSize=9,
        spaceAfter=6,
        fontName='Courier',
        leftIndent=20
    )
    
    # Build the story (content)
    story = []
    
    # Title page
    story.append(Paragraph("Metro Bus Route Planner Backend", title_style))
    story.append(Spacer(1, 20))
    story.append(Paragraph("Comprehensive Technology & Process Documentation", styles['Heading2']))
    story.append(Spacer(1, 30))
    story.append(Paragraph(f"Generated on: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", styles['Normal']))
    story.append(Spacer(1, 40))
    story.append(Paragraph("A complete guide to the technologies, architecture, and processes used in the Metro Bus Route Planner Backend system for Islamabad's Green and Blue Metro Bus lines.", styles['Normal']))
    story.append(PageBreak())
    
    # Table of Contents
    story.append(Paragraph("Table of Contents", heading1_style))
    story.append(Spacer(1, 20))
    
    toc_data = [
        ["Section", "Page"],
        ["1. Project Overview", "3"],
        ["2. Team Structure & Responsibilities", "4"],
        ["3. Technology Stack", "6"],
        ["4. System Architecture", "8"],
        ["5. Data Processing & Management", "10"],
        ["6. API Design & Implementation", "12"],
        ["7. AI Integration", "14"],
        ["8. Geographic Data Handling", "16"],
        ["9. Deployment & Infrastructure", "18"],
        ["10. Development Process", "20"],
        ["11. Testing & Quality Assurance", "22"],
        ["12. Performance & Scalability", "24"],
        ["13. Security Considerations", "26"],
        ["14. Future Enhancements", "28"]
    ]
    
    toc_table = Table(toc_data, colWidths=[3*inch, 1*inch])
    toc_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(toc_table)
    story.append(PageBreak())
    
    # 1. Project Overview
    story.append(Paragraph("1. Project Overview", heading1_style))
    story.append(Paragraph("""
        The Metro Bus Route Planner  is an intelligent, AI-powered route planning system designed specifically for 
        Islamabad's Metro Bus network. The system serves both the Green Line and Blue Line metro services, providing 
        passengers with optimal route recommendations, real-time scheduling information, and intelligent travel assistance.
    """, normal_style))
    
    story.append(Paragraph("Key Features:", heading2_style))
    story.append(Paragraph("""
        • Intelligent route planning between any two metro stops<br/>
        • AI-powered travel assistant with natural language processing<br/>
        • Real-time schedule management and optimization<br/>
        • Multi-line support (Green Line and Blue Line)<br/>
        • Geographic data integration using shapefiles<br/>
        • RESTful API for frontend applications<br/>
        • Comprehensive stop database management
    """, normal_style))
    
    story.append(Paragraph("Project Goals:", heading2_style))
    story.append(Paragraph("""
        • Improve public transportation accessibility in Islamabad<br/>
        • Reduce passenger confusion and travel time<br/>
        • Provide intelligent route recommendations<br/>
        • Support both English and local language interactions<br/>
        • Enable scalable deployment for future metro line expansions
    """, normal_style))
    story.append(PageBreak())
    
    # 2. Team Structure & Responsibilities
    story.append(Paragraph("2. Team Structure & Responsibilities", heading1_style))
    story.append(Paragraph("""
        The Metro Bus Route Planner Backend project is a collaborative effort involving a diverse team of developers, 
        designers, and domain experts. Each team member brings unique skills and perspectives to ensure the project's success.
    """, normal_style))
    
    story.append(Paragraph("2.1 Team Overview", heading2_style))
    story.append(Paragraph("""
        Our team consists of five dedicated members, each with specific roles and responsibilities that contribute to 
        different aspects of the project development lifecycle. This collaborative approach ensures comprehensive coverage 
        of technical, design, and user experience requirements.
    """, normal_style))
    
    story.append(Paragraph("2.2 Individual Responsibilities", heading2_style))
    
    # Team member responsibilities table
    team_data = [
        ["Team Member", "Role & Responsibilities", "Key Contributions"],
        ["AbdurRehman", "Project Lead & Data Architect", "• Project conception and initial implementation\n• Data gathering and research\n• System architecture design\n• Project coordination and planning"],
        ["Abdullah", "Core Developer & DevOps", "• Core system implementation\n• Backend development\n• Deployment and infrastructure\n• Technical architecture"],
        ["Zainab", "UX/UI Designer & Frontend", "• Design changes and improvements\n• Frontend development\n• User interface optimization\n• New user acquisition strategies"],
        ["Mahnoor", "User Experience Specialist", "• User experience improvement\n• User feedback analysis\n• Promotion and marketing\n• User engagement strategies"],
        ["Khadijah", "Business Analyst & User Insights", "• Detailed business insights\n• User behavior analysis\n• Market research\n• User acquisition strategies"]
    ]
    
    team_table = Table(team_data, colWidths=[1.5*inch, 2.0*inch, 2.0*inch])
    team_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.purple),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),  # Center align team member names
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),    # Left align roles
        ('ALIGN', (2, 0), (2, -1), 'LEFT'),    # Left align contributions
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('FONTSIZE', (0, 1), (-1, -1), 8),     # Smaller font for data rows
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lavender),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),   # Top align for better readability
        ('WRAP', (1, 0), (2, -1), True),       # Enable text wrapping
        ('LEFTPADDING', (1, 0), (2, -1), 6),   # Add left padding for content
        ('RIGHTPADDING', (1, 0), (2, -1), 6)   # Add right padding for content
    ]))
    story.append(team_table)
    story.append(Spacer(1, 25))
    
    story.append(Paragraph("2.3 Role Descriptions", heading2_style))
    
    story.append(Paragraph("<b>AbdurRehman - Project Lead & Data Architect:</b>", normal_style))
    story.append(Paragraph("""
        As the project lead, AbdurRehman is responsible for the overall project vision, initial implementation, and data gathering. 
        This includes researching metro bus systems, collecting geographic data, designing the system architecture, and coordinating 
        team efforts to ensure project milestones are met.
    """, normal_style))
    
    story.append(Paragraph("<b>Abdullah - Core Developer & DevOps:</b>", normal_style))
    story.append(Paragraph("""
        Abdullah handles the core implementation of the backend system, including API development, database design, and system 
        architecture. Additionally, manages deployment processes, infrastructure setup, and ensures the technical foundation 
        is robust and scalable.
    """, normal_style))
    
    story.append(Paragraph("<b>Zainab - UX/UI Designer & Frontend:</b>", normal_style))
    story.append(Paragraph("""
        Zainab focuses on user experience and interface design, implementing design changes, developing frontend components, 
        and optimizing user interactions. Plays a crucial role in attracting new users through intuitive and appealing design.
    """, normal_style))
    
    story.append(Paragraph("<b>Mahnoor - User Experience Specialist:</b>", normal_style))
    story.append(Paragraph("""
        Mahnoor specializes in improving overall user experience through feedback analysis, user engagement strategies, and 
        promotional activities. Ensures the system meets user needs and expectations while driving user adoption.
    """, normal_style))
    
    story.append(Paragraph("<b>Khadijah - Business Analyst & User Insights:</b>", normal_style))
    story.append(Paragraph("""
        Khadijah provides detailed business insights, analyzes user behavior patterns, conducts market research, and develops 
        strategies for user acquisition. Ensures the project aligns with business objectives and user needs.
    """, normal_style))
    
    story.append(Paragraph("2.4 Collaboration Model", heading2_style))
    story.append(Paragraph("""
        The team operates on a collaborative model where:<br/>
        • Regular communication ensures alignment on project goals<br/>
        • Cross-functional collaboration leverages diverse expertise<br/>
        • Iterative development incorporates feedback from all team members<br/>
        • Shared responsibility for project success and user satisfaction
    """, normal_style))
    story.append(PageBreak())
    
    # 3. Technology Stack
    story.append(Paragraph("3. Technology Stack", heading1_style))
    story.append(Paragraph("The project utilizes a modern, Python-based technology stack optimized for performance, scalability, and maintainability.", normal_style))
    
    story.append(Paragraph("3.1 Core Framework", heading2_style))
    story.append(Paragraph("""
        <b>FastAPI (v0.109.0):</b> Modern, fast web framework for building APIs with Python 3.7+ based on standard Python type hints. 
        Provides automatic API documentation, data validation, and high performance.
    """, normal_style))
    
    story.append(Paragraph("3.2 Web Server", heading2_style))
    story.append(Paragraph("""
        <b>Uvicorn (v0.27.0):</b> Lightning-fast ASGI server implementation, used for running FastAPI applications with 
        support for WebSocket, HTTP/2, and other modern web protocols.
    """, normal_style))
    
    story.append(Paragraph("3.3 Data Validation & Serialization", heading2_style))
    story.append(Paragraph("""
        <b>Pydantic (v2.5.0):</b> Data validation and settings management using Python type annotations. 
        Ensures data integrity and provides automatic serialization/deserialization.
    """, normal_style))
    
    story.append(Paragraph("3.4 AI Integration", heading2_style))
    story.append(Paragraph("""
        <b>Google Generative AI (v1.28.0):</b> Integration with Google's Gemini AI model for intelligent 
        route planning assistance and natural language processing capabilities.
    """, normal_style))
    
    story.append(Paragraph("3.5 Geographic Data Processing", heading2_style))
    story.append(Paragraph("""
        <b>PyShp (v2.3.1):</b> Pure Python library for reading and writing ESRI shapefiles, used for 
        processing metro station geographic data and coordinates.
    """, normal_style))
    
    story.append(Paragraph("3.6 Utility Libraries", heading2_style))
    story.append(Paragraph("""
        • <b>python-multipart:</b> File upload support for multipart/form-data<br/>
        • <b>PyPDF2:</b> PDF processing capabilities<br/>
        • <b>python-dateutil:</b> Date and time utilities<br/>
        • <b>python-dotenv:</b> Environment variable management
    """, normal_style))
    story.append(PageBreak())
    
    # 4. System Architecture
    story.append(Paragraph("4. System Architecture", heading1_style))
    story.append(Paragraph("The system follows a modular, service-oriented architecture designed for scalability and maintainability.", normal_style))
    
    story.append(Paragraph("4.1 High-Level Architecture", heading2_style))
    story.append(Paragraph("""
        The system is organized into several key components that work together to provide comprehensive route planning services:
    """, normal_style))
    
    architecture_data = [
        ["Component", "Purpose", "Technology"],
        ["API Gateway", "HTTP request handling & routing", "FastAPI + Uvicorn"],
        ["Route Planner", "Core routing algorithms", "Custom Python logic"],
        ["AI Assistant", "Intelligent travel guidance", "Google Gemini AI"],
        ["Stops Database", "Station & route data management", "Shapefile + JSON"],
        ["Data Processor", "Geographic data extraction", "PyShp + Custom scripts"],
        ["Models", "Data structures & validation", "Pydantic models"]
    ]
    
    arch_table = Table(architecture_data, colWidths=[1.5*inch, 2.5*inch, 1.5*inch])
    arch_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
    ]))
    story.append(arch_table)
    story.append(Spacer(1, 20))
    
    story.append(Paragraph("4.2 Data Flow Architecture", heading2_style))
    story.append(Paragraph("""
        1. <b>Input Layer:</b> HTTP requests from clients (web/mobile apps)<br/>
        2. <b>API Layer:</b> FastAPI handles request validation and routing<br/>
        3. <b>Business Logic:</b> Route planning algorithms and AI processing<br/>
        4. <b>Data Layer:</b> Geographic data and route information storage<br/>
        5. <b>Output Layer:</b> Structured JSON responses with route plans
    """, normal_style))
    story.append(PageBreak())
    
    # 5. Data Processing & Management
    story.append(Paragraph("5. Data Processing & Management", heading1_style))
    story.append(Paragraph("The system handles multiple types of data sources and formats to provide accurate route planning services.", normal_style))
    
    story.append(Paragraph("5.1 Geographic Data Sources", heading2_style))
    story.append(Paragraph("""
        <b>Shapefiles (.shp):</b> ESRI shapefile format containing metro station coordinates and metadata<br/>
        • Green Line: GREEN_STATIONS.shp with station locations and properties<br/>
        • Blue Line: BLUE_STATIONS.shp with station locations and properties<br/>
        • Includes projection files (.prj) for coordinate system information
    """, normal_style))
    
    story.append(Paragraph("5.2 Route Data", heading2_style))
    story.append(Paragraph("""
        <b>JSON Route Analysis:</b> Comprehensive route information stored in routes_analysis.json<br/>
        • Trip schedules and timing information<br/>
        • Stop sequences and transfer points<br/>
        • Route metadata and operational details
    """, normal_style))
    
    story.append(Paragraph("5.3 Data Processing Pipeline", heading2_style))
    story.append(Paragraph("""
        1. <b>Shapefile Extraction:</b> PyShp library reads geographic data<br/>
        2. <b>Coordinate Processing:</b> Latitude/longitude extraction and validation<br/>
        3. <b>Stop Mapping:</b> Integration between shapefile names and route names<br/>
        4. <b>Data Validation:</b> Pydantic models ensure data integrity<br/>
        5. <b>Database Population:</b> In-memory database for fast access
    """, normal_style))
    
    story.append(Paragraph("5.4 Data Models", heading2_style))
    story.append(Paragraph("""
        The system uses strongly-typed data models for all entities:<br/>
        • <b>Station:</b> Geographic location, line affiliation, interchange status<br/>
        • <b>Route:</b> Trip information, timing, direction<br/>
        • <b>RoutePlan:</b> Complete journey with segments and instructions<br/>
        • <b>MetroLine:</b> Line identification (GREEN/BLUE) with metadata
    """, normal_style))
    story.append(PageBreak())
    
    # 6. API Design & Implementation
    story.append(Paragraph("6. API Design & Implementation", heading1_style))
    story.append(Paragraph("The system provides a comprehensive RESTful API designed for ease of use and integration.", normal_style))
    
    story.append(Paragraph("6.1 API Endpoints", heading2_style))
    
    endpoints_data = [
        ["Endpoint", "Method", "Purpose", "Response"],
        ["/", "GET", "Health check & status", "Service information"],
        ["/health", "GET", "Detailed health status", "System health metrics"],
        ["/plan-route", "POST", "Route planning", "Route plans & alternatives"],
        ["/stops", "GET", "Available stops", "Stop list & metadata"],
        ["/chat", "POST", "AI assistance", "Intelligent responses"],
        ["/check-routes-file", "GET", "Data file status", "File existence & size"]
    ]
    
    endpoints_table = Table(endpoints_data, colWidths=[1.2*inch, 0.8*inch, 2*inch, 1.5*inch])
    endpoints_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkgreen),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgreen),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
    ]))
    story.append(endpoints_table)
    story.append(Spacer(1, 20))
    
    story.append(Paragraph("6.2 Request/Response Models", heading2_style))
    story.append(Paragraph("""
        <b>Route Planning Request:</b><br/>
        • Origin and destination locations<br/>
        • Preferred departure time<br/>
        • Maximum wait time preferences<br/>
        • Metro line preferences (GREEN/BLUE)
    """, normal_style))
    
    story.append(Paragraph("""
        <b>Route Planning Response:</b><br/>
        • Success/failure status<br/>
        • Detailed route plans with segments<br/>
        • Alternative route options<br/>
        • Journey instructions and timing
    """, normal_style))
    
    story.append(Paragraph("6.3 API Features", heading2_style))
    story.append(Paragraph("""
        • <b>Automatic Documentation:</b> OpenAPI/Swagger UI integration<br/>
        • <b>CORS Support:</b> Cross-origin resource sharing enabled<br/>
        • <b>Input Validation:</b> Pydantic-based request validation<br/>
        • <b>Error Handling:</b> Comprehensive HTTP error responses<br/>
        • <b>Type Safety:</b> Full type hints and validation
    """, normal_style))
    story.append(PageBreak())
    
    # 7. AI Integration
    story.append(Paragraph("7. AI Integration", heading1_style))
    story.append(Paragraph("The system leverages Google's Gemini AI to provide intelligent travel assistance and route optimization.", normal_style))
    
    story.append(Paragraph("7.1 AI Assistant Architecture", heading2_style))
    story.append(Paragraph("""
        The AIAssistant class integrates with Google's Generative AI API to provide:<br/>
        • Natural language route planning assistance<br/>
        • Intelligent travel recommendations<br/>
        • Context-aware responses based on route data<br/>
        • Multi-language support capabilities
    """, normal_style))
    
    story.append(Paragraph("7.2 System Prompt Design", heading2_style))
    story.append(Paragraph("""
        The AI is configured with a specialized system prompt that defines its role as a friendly conductor/travel guide:<br/>
        • Route finding assistance<br/>
        • Clear travel instructions<br/>
        • Schedule and timing information<br/>
        • Travel tips and advice<br/>
        • Patient and understanding responses
    """, normal_style))
    
    story.append(Paragraph("7.3 AI Processing Flow", heading2_style))
    story.append(Paragraph("""
        1. <b>User Input:</b> Natural language query received<br/>
        2. <b>Context Enrichment:</b> Route data and user preferences added<br/>
        3. <b>AI Processing:</b> Gemini model generates contextual response<br/>
        4. <b>Response Formatting:</b> Structured output with route suggestions<br/>
        5. <b>User Delivery:</b> Intelligent response with actionable information
    """, normal_style))
    
    story.append(Paragraph("7.4 AI Capabilities", heading2_style))
    story.append(Paragraph("""
        • <b>Route Optimization:</b> Suggests best routes based on preferences<br/>
        • <b>Natural Language:</b> Understands conversational queries<br/>
        • <b>Context Awareness:</b> Considers current route planning data<br/>
        • <b>Multi-modal Support:</b> Can handle various input formats<br/>
        • <b>Learning Capability:</b> Improves responses over time
    """, normal_style))
    story.append(PageBreak())
    
    # 8. Geographic Data Handling
    story.append(Paragraph("8. Geographic Data Handling", heading1_style))
    story.append(Paragraph("The system processes and manages complex geographic data to provide accurate location-based services.", normal_style))
    
    story.append(Paragraph("8.1 Shapefile Processing", heading2_style))
    story.append(Paragraph("""
        <b>Data Extraction:</b> PyShp library processes ESRI shapefiles<br/>
        • Station coordinates (latitude/longitude)<br/>
        • Station metadata (names, IDs, line codes)<br/>
        • Interchange station identification<br/>
        • Projection and coordinate system information
    """, normal_style))
    
    story.append(Paragraph("8.2 Coordinate Management", heading2_style))
    story.append(Paragraph("""
        • <b>Coordinate Extraction:</b> Latitude and longitude from shapefile points<br/>
        • <b>Projection Handling:</b> Support for various coordinate systems<br/>
        • <b>Data Validation:</b> Coordinate range and format validation<br/>
        • <b>Spatial Indexing:</b> Efficient geographic data retrieval
    """, normal_style))
    
    story.append(Paragraph("8.3 Station Mapping", heading2_style))
    story.append(Paragraph("""
        The system maintains comprehensive mapping between:<br/>
        • Shapefile station names and route names<br/>
        • Station IDs and geographic coordinates<br/>
        • Line affiliations and interchange status<br/>
        • Stop sequences and timing information
    """, normal_style))
    
    story.append(Paragraph("8.4 Data Integration", heading2_style))
    story.append(Paragraph("""
        Geographic data is integrated with route planning through:<br/>
        • <b>Stop Database:</b> Centralized station information management<br/>
        • <b>Route Matching:</b> Geographic location to route association<br/>
        • <b>Transfer Points:</b> Interchange station identification<br/>
        • <b>Distance Calculations:</b> Geographic distance-based routing
    """, normal_style))
    story.append(PageBreak())
    
    # 9. Deployment & Infrastructure
    story.append(Paragraph("9. Deployment & Infrastructure", heading1_style))
    story.append(Paragraph("The system is designed for cloud deployment with support for multiple hosting platforms.", normal_style))
    
    story.append(Paragraph("9.1 Vercel Deployment", heading2_style))
    story.append(Paragraph("""
        <b>Configuration:</b> vercel.json defines build and routing settings<br/>
        • Python runtime with @vercel/python builder<br/>
        • Automatic routing for all endpoints<br/>
        • Serverless function deployment<br/>
        • Global CDN distribution
    """, normal_style))
    
    story.append(Paragraph("9.2 Environment Management", heading2_style))
    story.append(Paragraph("""
        • <b>Environment Variables:</b> python-dotenv for configuration management<br/>
        • <b>API Keys:</b> Secure storage of external service credentials<br/>
        • <b>Configuration:</b> Environment-specific settings<br/>
        • <b>Secrets Management:</b> Secure handling of sensitive data
    """, normal_style))
    
    story.append(Paragraph("9.3 Scaling Considerations", heading2_style))
    story.append(Paragraph("""
        • <b>Serverless Architecture:</b> Automatic scaling based on demand<br/>
        • <b>Stateless Design:</b> No persistent server state<br/>
        • <b>CDN Integration:</b> Global content delivery<br/>
        • <b>Load Balancing:</b> Automatic traffic distribution
    """, normal_style))
    
    story.append(Paragraph("9.4 Monitoring & Health Checks", heading2_style))
    story.append(Paragraph("""
        • <b>Health Endpoints:</b> / and /health for system monitoring<br/>
        • <b>Status Reporting:</b> Service availability and performance metrics<br/>
        • <b>Error Handling:</b> Comprehensive error logging and reporting<br/>
        • <b>Performance Metrics:</b> Response time and throughput monitoring
    """, normal_style))
    story.append(PageBreak())
    
    # 10. Development Process
    story.append(Paragraph("10. Development Process", heading1_style))
    story.append(Paragraph("The project follows modern software development practices and methodologies.", normal_style))
    
    story.append(Paragraph("10.1 Development Workflow", heading2_style))
    story.append(Paragraph("""
        • <b>Modular Design:</b> Separation of concerns with dedicated modules<br/>
        • <b>Type Safety:</b> Comprehensive type hints and validation<br/>
        • <b>Error Handling:</b> Robust exception handling throughout<br/>
        • <b>Code Organization:</b> Clear file structure and naming conventions
    """, normal_style))
    
    story.append(Paragraph("10.2 Testing Strategy", heading2_style))
    story.append(Paragraph("""
        • <b>Unit Testing:</b> Individual component testing<br/>
        • <b>Integration Testing:</b> API endpoint testing<br/>
        • <b>Data Validation Testing:</b> Shapefile and route data testing<br/>
        • <b>Performance Testing:</b> Route planning algorithm testing
    """, normal_style))
    
    story.append(Paragraph("10.3 Code Quality", heading2_style))
    story.append(Paragraph("""
        • <b>Documentation:</b> Comprehensive code comments and docstrings<br/>
        • <b>Error Handling:</b> Graceful error handling and user feedback<br/>
        • <b>Logging:</b> Structured logging for debugging and monitoring<br/>
        • <b>Code Standards:</b> PEP 8 compliance and best practices
    """, normal_style))
    
    story.append(Paragraph("10.4 Version Control", heading2_style))
    story.append(Paragraph("""
        • <b>Git Repository:</b> Source code version control<br/>
        • <b>Branch Management:</b> Feature and development branches<br/>
        • <b>Commit History:</b> Detailed change tracking<br/>
        • <b>Collaboration:</b> Team development support
    """, normal_style))
    story.append(PageBreak())
    
    # 11. Testing & Quality Assurance
    story.append(Paragraph("11. Testing & Quality Assurance", heading1_style))
    story.append(Paragraph("Comprehensive testing ensures system reliability and performance.", normal_style))
    
    story.append(Paragraph("11.1 Testing Framework", heading2_style))
    story.append(Paragraph("""
        • <b>Python Testing:</b> Built-in unittest framework<br/>
        • <b>API Testing:</b> Endpoint validation and response testing<br/>
        • <b>Data Testing:</b> Shapefile processing and validation<br/>
        • <b>Integration Testing:</b> End-to-end system testing
    """, normal_style))
    
    story.append(Paragraph("11.2 Test Coverage", heading2_style))
    story.append(Paragraph("""
        • <b>Unit Tests:</b> Individual function and class testing<br/>
        • <b>API Tests:</b> HTTP endpoint testing (test_api.py)<br/>
        • <b>Database Tests:</b> Stops database functionality testing<br/>
        • <b>Route Tests:</b> Route planning algorithm testing<br/>
        • <b>System Tests:</b> Complete workflow testing
    """, normal_style))
    
    story.append(Paragraph("11.3 Quality Metrics", heading2_style))
    story.append(Paragraph("""
        • <b>Code Coverage:</b> Comprehensive test coverage<br/>
        • <b>Performance Metrics:</b> Response time and throughput<br/>
        • <b>Error Rates:</b> System reliability monitoring<br/>
        • <b>User Experience:</b> API usability and documentation
    """, normal_style))
    
    story.append(Paragraph("11.4 Continuous Integration", heading2_style))
    story.append(Paragraph("""
        • <b>Automated Testing:</b> Test execution on code changes<br/>
        • <b>Quality Gates:</b> Minimum quality standards enforcement<br/>
        • <b>Deployment Validation:</b> Pre-deployment testing<br/>
        • <b>Performance Monitoring:</b> Ongoing system performance tracking
    """, normal_style))
    story.append(PageBreak())
    
    # 12. Performance & Scalability
    story.append(Paragraph("12. Performance & Scalability", heading1_style))
    story.append(Paragraph("The system is designed for high performance and scalability to handle growing user demands.", normal_style))
    
    story.append(Paragraph("12.1 Performance Optimizations", heading2_style))
    story.append(Paragraph("""
        • <b>In-Memory Database:</b> Fast data access for route planning<br/>
        • <b>Efficient Algorithms:</b> Optimized route planning algorithms<br/>
        • <b>Data Caching:</b> Frequently accessed data caching<br/>
        • <b>Response Optimization:</b> Minimal response payload sizes
    """, normal_style))
    
    story.append(Paragraph("12.2 Scalability Features", heading2_style))
    story.append(Paragraph("""
        • <b>Stateless Design:</b> No server state for horizontal scaling<br/>
        • <b>Modular Architecture:</b> Independent component scaling<br/>
        • <b>Load Distribution:</b> Automatic traffic distribution<br/>
        • <b>Resource Management:</b> Efficient memory and CPU usage
    """, normal_style))
    
    story.append(Paragraph("12.3 Monitoring & Metrics", heading2_style))
    story.append(Paragraph("""
        • <b>Response Time Tracking:</b> API endpoint performance monitoring<br/>
        • <b>Throughput Monitoring:</b> Request handling capacity<br/>
        • <b>Resource Utilization:</b> CPU and memory usage tracking<br/>
        • <b>Error Rate Monitoring:</b> System reliability metrics
    """, normal_style))
    
    story.append(Paragraph("12.4 Future Scaling", heading2_style))
    story.append(Paragraph("""
        • <b>Database Scaling:</b> Support for larger datasets<br/>
        • <b>API Rate Limiting:</b> Request throttling and management<br/>
        • <b>Microservices Architecture:</b> Component separation for scaling<br/>
        • <b>Load Balancing:</b> Advanced traffic distribution strategies
    """, normal_style))
    story.append(PageBreak())
    
    # 13. Security Considerations
    story.append(Paragraph("13. Security Considerations", heading1_style))
    story.append(Paragraph("Security is a critical aspect of the system design and implementation.", normal_style))
    
    story.append(Paragraph("13.1 API Security", heading2_style))
    story.append(Paragraph("""
        • <b>Input Validation:</b> Comprehensive request validation<br/>
        • <b>Type Safety:</b> Strong typing prevents injection attacks<br/>
        • <b>Error Handling:</b> Secure error message generation<br/>
        • <b>Rate Limiting:</b> Protection against abuse and DoS attacks
    """, normal_style))
    
    story.append(Paragraph("13.2 Data Security", heading2_style))
    story.append(Paragraph("""
        • <b>Environment Variables:</b> Secure credential management<br/>
        • <b>Data Validation:</b> Input sanitization and validation<br/>
        • <b>Access Control:</b> API endpoint access management<br/>
        • <b>Data Encryption:</b> Sensitive data protection
    """, normal_style))
    
    story.append(Paragraph("13.3 Infrastructure Security", heading2_style))
    story.append(Paragraph("""
        • <b>HTTPS Enforcement:</b> Secure communication protocols<br/>
        • <b>CORS Configuration:</b> Controlled cross-origin access<br/>
        • <b>Server Security:</b> Platform-level security features<br/>
        • <b>Monitoring:</b> Security event detection and logging
    """, normal_style))
    
    story.append(Paragraph("13.4 Best Practices", heading2_style))
    story.append(Paragraph("""
        • <b>Principle of Least Privilege:</b> Minimal required permissions<br/>
        • <b>Regular Updates:</b> Dependency and security updates<br/>
        • <b>Security Auditing:</b> Regular security assessments<br/>
        • <b>Incident Response:</b> Security incident handling procedures
    """, normal_style))
    story.append(PageBreak())
    
    # 14. Future Enhancements
    story.append(Paragraph("14. Future Enhancements", heading1_style))
    story.append(Paragraph("The system is designed with future growth and enhancement capabilities in mind.", normal_style))
    
    story.append(Paragraph("14.1 Feature Enhancements", heading2_style))
    story.append(Paragraph("""
        • <b>Real-time Updates:</b> Live bus location and timing updates<br/>
        • <b>Multi-language Support:</b> Local language interface support<br/>
        • <b>Mobile Applications:</b> Native mobile app development<br/>
        • <b>User Accounts:</b> Personalized route preferences and history
    """, normal_style))
    
    story.append(Paragraph("14.2 Technical Improvements", heading2_style))
    story.append(Paragraph("""
        • <b>Machine Learning:</b> Route optimization based on usage patterns<br/>
        • <b>Predictive Analytics:</b> Demand forecasting and capacity planning<br/>
        • <b>Advanced AI:</b> Enhanced natural language processing<br/>
        • <b>Performance Optimization:</b> Algorithm and data structure improvements
    """, normal_style))
    
    story.append(Paragraph("14.3 Infrastructure Scaling", heading2_style))
    story.append(Paragraph("""
        • <b>Database Migration:</b> Persistent database implementation<br/>
        • <b>Microservices:</b> Component separation for independent scaling<br/>
        • <b>Containerization:</b> Docker and Kubernetes deployment<br/>
        • <b>Cloud Migration:</b> Multi-cloud and hybrid cloud support
    """, normal_style))
    
    story.append(Paragraph("14.4 Integration Capabilities", heading2_style))
    story.append(Paragraph("""
        • <b>Third-party APIs:</b> Weather, traffic, and event data integration<br/>
        • <b>Payment Systems:</b> Ticket booking and payment processing<br/>
        • <b>Social Features:</b> Community-driven route recommendations<br/>
        • <b>Analytics Dashboard:</b> Comprehensive system usage analytics
    """, normal_style))
    
    # Conclusion
    story.append(PageBreak())
    story.append(Paragraph("Conclusion", heading1_style))
    story.append(Paragraph("""
        The Metro Bus Route Planner Backend represents a comprehensive, modern approach to public transportation 
        route planning. By combining cutting-edge technologies like FastAPI, AI integration, and geographic data 
        processing, the system provides a robust foundation for intelligent transportation services.
    """, normal_style))
    
    story.append(Paragraph("""
        The project demonstrates best practices in software architecture, data management, and API design, 
        while maintaining a clear focus on user experience and system reliability. With its modular design 
        and scalable architecture, the system is well-positioned for future growth and enhancement.
    """, normal_style))
    
    story.append(Paragraph("""
        The collaborative team effort, with each member contributing their unique expertise, has resulted in a 
        system that not only meets technical requirements but also addresses real-world user needs. As public 
        transportation systems continue to evolve, this platform provides the technological foundation needed 
        to support modern, intelligent transportation services that improve accessibility, reduce travel time, 
        and enhance the overall passenger experience.
    """, normal_style))
    
    # Build the PDF
    doc.build(story)
    print("Updated PDF documentation created successfully: Metro_Bus_Route_Planner_Backend_Documentation_Updated.pdf")

if __name__ == "__main__":
    try:
        create_updated_project_documentation()
    except Exception as e:
        print(f"Error creating PDF: {e}")
        import traceback
        traceback.print_exc()
