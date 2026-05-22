# Odoo 18 Tender Management Module

## Overview
A comprehensive tender and bidding management system for Odoo 18 ERP designed to streamline the procurement process through announcement, bidding, evaluation, and approval workflows.

## Features

### Core Features
- **Tender Announcements**: Create and manage tender announcements with detailed specifications
- **Bid Acceptance**: Accept or reject bid submissions from vendors
- **Bid Management**: Track and manage multiple bids for each tender
- **Vendor Management**: Maintain vendor profiles with performance tracking
- **Bid Evaluation**: Comprehensive evaluation system with multiple scoring criteria
- **Approval Workflow**: Multi-level approval process for tender awards

### Advanced Features
- **Evaluation Criteria**: Price, quality, delivery time, technical capability scoring
- **Vendor Ratings**: Performance tracking and ratings
- **Compliance Tracking**: Tax and insurance compliance verification
- **Certifications**: Vendor certification management
- **Reports**: Tender summary, bid comparison, and vendor performance reports
- **Security**: Role-based access control with multiple user groups

## User Roles

### Tender User
- View assigned tenders and bids
- Basic read-only access

### Tender Manager
- Create and manage tender announcements
- Publish tenders and manage bidding periods
- Manage vendor information
- Full CRUD operations on tenders and items

### Tender Evaluator
- Evaluate bids with scoring system
- Review bid compliance
- Generate evaluation reports

### Tender Approver
- Review evaluations
- Approve final tender awards
- Multi-level approval authority

## Models

### Tender Announcement
- Title, description, and tender type (open/closed/limited/single)
- Budget and timeline information
- Tender items with quantity and specifications
- Approved vendor list
- Document attachments

### Tender Bid
- Vendor information and bid date
- Bid items with pricing
- Evaluation scores (price, quality, delivery, technical)
- Payment terms and warranty information
- Bid attachments

### Tender Evaluation
- Configurable evaluation criteria weights
- Scoring for each bid
- Best bid and price bid tracking
- Evaluation recommendation

### Tender Approval
- Multi-level approval chain
- Approval status tracking
- Winner selection
- Audit trail with timestamps

### Tender Vendor
- Vendor profile and performance metrics
- Compliance status (tax, insurance)
- Certifications and ratings
- Bid history and success rates

## Installation

1. Clone this repository into your Odoo addons directory
2. Update the module list in Odoo
3. Install the "Tender Management" module
4. Assign user groups as appropriate

## Configuration

### Initial Setup
1. Create vendor profiles in Vendor Management
2. Define tender types and categories
3. Set up department associations
4. Configure approval workflows

### Evaluation Weights
Customize evaluation criteria weights in each evaluation form:
- Price Weight (default: 40%)
- Quality Weight (default: 30%)
- Delivery Weight (default: 20%)
- Technical Weight (default: 10%)

## Workflows

### Tender Lifecycle
1. **Draft**: Initial tender creation
2. **Published**: Tender announced to vendors
3. **Open**: Actively accepting bids
4. **Closed**: Bid submission period ended
5. **Awarded**: Tender awarded to winning vendor
6. **Rejected**: Tender cancelled or all bids rejected

### Bid Status Flow
1. **Draft**: Initial bid entry
2. **Submitted**: Vendor submitted bid
3. **Qualified**: Bid meets minimum requirements
4. **Selected**: Bid selected as winner (post-approval)
5. **Rejected**: Bid disqualified

### Approval Process
1. **Pending**: Awaiting approval initiation
2. **Under Review**: In approval chain
3. **Approved**: All approval levels completed
4. **Rejected**: Rejected at any approval level

## Reports

- **Tender Report**: Complete tender details and specifications
- **Bid Comparison Report**: Side-by-side bid analysis
- **Evaluation Report**: Detailed scoring and rankings
- **Vendor Performance Report**: Vendor metrics and history

## Support

For issues or feature requests, please create an issue in the repository.

## License

This module is licensed under the LGPL-3 license.
