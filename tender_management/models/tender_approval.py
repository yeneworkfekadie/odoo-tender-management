from odoo import models, fields, api

class TenderApproval(models.Model):
    _name = 'tender.approval'
    _description = 'Tender Approval Workflow'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    tender_id = fields.Many2one('tender.announcement', 'Tender', required=True, ondelete='cascade')
    evaluation_id = fields.Many2one('tender.evaluation', 'Evaluation', required=True, ondelete='cascade')
    
    status = fields.Selection([
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('under_review', 'Under Review'),
    ], default='pending', track_visibility='onchange')
    
    # Approval Chain
    approval_lines = fields.One2many('tender.approval.line', 'approval_id', 'Approval Levels')
    
    # Winner Details
    winning_bid_id = fields.Many2one('tender.bid', 'Winning Bid')
    winner_vendor_id = fields.Many2one('res.partner', 'Winner Vendor')
    
    # Final Details
    approval_date = fields.Datetime('Approval Date')
    approved_by = fields.Many2one('res.users', 'Approved By')
    approval_notes = fields.Text('Approval Notes')
    
    company_id = fields.Many2one('res.company', related='tender_id.company_id', readonly=True)
    
    def action_send_for_approval(self):
        """Send to first level of approval"""
        self.write({'status': 'under_review'})
        return True
    
    def action_approve(self):
        self.write({
            'status': 'approved',
            'approval_date': fields.Datetime.now(),
            'approved_by': self.env.user.id,
        })
        # Update tender status
        self.tender_id.write({'status': 'awarded'})
        return True
    
    def action_reject(self):
        self.write({'status': 'rejected'})
        self.tender_id.write({'status': 'rejected'})
        return True


class TenderApprovalLine(models.Model):
    _name = 'tender.approval.line'
    _description = 'Tender Approval Line'
    _order = 'sequence'

    approval_id = fields.Many2one('tender.approval', 'Approval', ondelete='cascade')
    sequence = fields.Integer('Sequence', default=10)
    
    approval_level = fields.Selection([
        ('department_head', 'Department Head'),
        ('procurement', 'Procurement Manager'),
        ('finance', 'Finance Manager'),
        ('executive', 'Executive Director'),
    ], required=True)
    
    approver_id = fields.Many2one('res.users', 'Approver', required=True)
    status = fields.Selection([
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], default='pending', track_visibility='onchange')
    
    approval_date = fields.Datetime('Approval Date')
    comments = fields.Text('Comments')
    
    def action_approve(self):
        self.write({
            'status': 'approved',
            'approval_date': fields.Datetime.now(),
        })
        return True
    
    def action_reject(self):
        self.write({
            'status': 'rejected',
            'approval_date': fields.Datetime.now(),
        })
        return True
