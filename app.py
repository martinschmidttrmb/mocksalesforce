"""
Mock Salesforce App using Streamlit
==================================
This application creates a mock Salesforce interface that allows you to:
- View and edit different Salesforce objects (Account, Contact, Opportunity, etc.)
- Configure which fields are visible and their order
- Share with team members for collaboration

Author: Assistant for Vibe Coder
"""

import streamlit as st
import pandas as pd
import json
from typing import Dict, List, Any
from dataclasses import dataclass, asdict
from datetime import datetime, date

# Page configuration - makes the app look more professional
st.set_page_config(
    page_title="Mock Salesforce",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS to make it look more like Salesforce
st.markdown("""
<style>
    /* Main Salesforce-like styling */
    .main > div {
        padding-top: 2rem;
    }
    
    .sf-header {
        background-color: #1B96FF;
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    
    .sf-object-header {
        background-color: #F3F3F3;
        padding: 1rem;
        border-radius: 0.25rem;
        border-left: 4px solid #1B96FF;
        margin-bottom: 1rem;
    }
    
    .field-container {
        border: 1px solid #D8DDE6;
        border-radius: 0.25rem;
        padding: 1rem;
        margin: 0.5rem 0;
        background-color: white;
    }
    
    .field-label {
        font-weight: 600;
        color: #3E3E3C;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.025rem;
        margin-bottom: 0.25rem;
    }
    
    .sidebar .sidebar-content {
        background-color: #F7F9FB;
    }
</style>
""", unsafe_allow_html=True)

@dataclass
class FieldConfig:
    """Configuration for each field in a Salesforce object"""
    name: str
    label: str
    field_type: str  # text, email, phone, picklist, date, number, checkbox, percentage, etc.
    visible: bool = True
    required: bool = False
    order: int = 0
    options: List[str] = None  # For picklist fields
    section: str = "General"  # Section grouping for fields
    
    def __post_init__(self):
        if self.options is None:
            self.options = []

@dataclass 
class SalesforceObject:
    """Represents a Salesforce object like Account, Contact, etc."""
    name: str
    label: str
    fields: List[FieldConfig]
    records: List[Dict[str, Any]]
    
class MockSalesforceApp:
    """Main application class for the Mock Salesforce interface"""
    
    def __init__(self):
        """Initialize the app with default objects and data"""
        self.init_session_state()
        self.load_default_objects()
    
    def init_session_state(self):
        """Initialize Streamlit session state variables"""
        if 'current_object' not in st.session_state:
            st.session_state.current_object = 'Account'
        
        if 'objects' not in st.session_state:
            st.session_state.objects = {}
            
        if 'editing_record' not in st.session_state:
            st.session_state.editing_record = None
    
    def load_default_objects(self):
        """Load default Salesforce objects with sample data matching the screenshot"""
        
        # Account object - matching the screenshot structure
        account_fields = [
            # Account Information Section - Left Column
            FieldConfig("account_name", "Account Name", "text", True, True, 1, section="Account Information"),
            FieldConfig("enterprise_account_number", "Enterprise Account Number", "text", True, False, 2, section="Account Information"),
            FieldConfig("division", "Division", "text", True, False, 3, section="Account Information"),
            FieldConfig("type", "Type", "picklist", True, False, 4, ["Customer", "Partner", "Prospect", "Vendor"], "Account Information"),
            FieldConfig("account_status_tmw", "Account Status TMW", "picklist", True, False, 5, 
                       ["CUSTOMER-(C) Live Customer", "PROSPECT-(P) Prospect", "INACTIVE-(I) Inactive"], "Account Information"),
            FieldConfig("tags", "Tags", "text", True, False, 6, section="Account Information"),
            FieldConfig("lead_source", "Lead Source", "text", True, False, 7, section="Account Information"),
            FieldConfig("trimble_tms_customer", "Trimble TMS Customer", "checkbox", True, False, 8, section="Account Information"),
            FieldConfig("global_id", "Global ID", "text", True, False, 9, section="Account Information"),
            FieldConfig("customer_profile", "Customer Profile", "text", True, False, 10, section="Account Information"),
            FieldConfig("account_stage_tmw_us", "Account Stage TMW US", "text", True, False, 11, section="Account Information"),
            FieldConfig("account_stage_tmw_aud", "Account Stage TMW AUD", "text", True, False, 12, section="Account Information"),
            
            # Account Information Section - Right Column
            FieldConfig("customer_id_tmw_us", "Customer Id TMW US", "text", True, False, 13, section="Account Information"),
            FieldConfig("customer_id_tmw_cad", "Customer Id TMW CAD", "text", True, False, 14, section="Account Information"),
            FieldConfig("customer_id_tmw_aud", "Customer Id TMW AUD", "text", True, False, 15, section="Account Information"),
            FieldConfig("parent_or_child_account", "Parent or Child Account", "picklist", True, False, 16, 
                       ["Parent", "Child"], "Account Information"),
            FieldConfig("account_timezone", "Account Time Zone (US & CA)", "picklist", True, False, 17,
                       ["Eastern Standard Time", "Central Standard Time", "Mountain Standard Time", "Pacific Standard Time"], 
                       "Account Information"),
            FieldConfig("phone_tmw", "Phone TMW", "phone", True, False, 18, section="Account Information"),
            FieldConfig("fax_tmw", "Fax TMW", "phone", True, False, 19, section="Account Information"),
            FieldConfig("website", "Website", "url", True, False, 20, section="Account Information"),
            FieldConfig("lead_source_detail", "Lead Source Detail", "text", True, False, 21, section="Account Information"),
            FieldConfig("support_maintenance", "Support & Maintenance", "percentage", True, False, 22, section="Account Information"),
            FieldConfig("customer_drive_link", "Customer Drive Link", "url", True, False, 23, section="Account Information"),
            FieldConfig("account_stage_tmw_cad", "Account Stage TMW CAD", "picklist", True, False, 24,
                       ["Customer", "Prospect", "Lead"], "Account Information"),
            
            # Parent Hierarchy Section
            FieldConfig("parent_account_tmw_us", "Parent Account TMW US", "text", False, False, 25, section="Parent Hierarchy"),
            FieldConfig("parent_account_tmw_cad", "Parent Account TMW CAD", "text", False, False, 26, section="Parent Hierarchy"),
            FieldConfig("parent_account", "Parent Account", "text", False, False, 27, section="Parent Hierarchy"),
            FieldConfig("parent_netsuite_id", "Parent NetSuite Id", "text", False, False, 28, section="Parent Hierarchy"),
            
            # Customer Success Section
            FieldConfig("customer_sentiment", "Customer Sentiment", "picklist", False, False, 29,
                       ["Excellent", "Good", "Average", "Poor", "Very Poor"], "Customer Success"),
            FieldConfig("enterprise_risk_status", "Enterprise Risk Status", "text", False, False, 30, section="Customer Success"),
            FieldConfig("enterprise_risk_reason", "Enterprise Risk Reason", "text", False, False, 31, section="Customer Success"),
            FieldConfig("enterprise_atrisk_severity", "Enterprise At-Risk Severity Level", "text", False, False, 32, section="Customer Success"),
            FieldConfig("enterprise_product_atrisk", "Enterprise Product At Risk", "text", False, False, 33, section="Customer Success"),
            FieldConfig("segmentation_tier", "Segmentation Tier", "picklist", False, False, 34,
                       ["Tier 1 Strategic", "Tier 2 Enterprise", "Tier 3 SMB", "Tier 4 Transactional", "Tier 5 CS Engage"], 
                       "Customer Success"),
            FieldConfig("at_risk_update", "At Risk Update", "text", False, False, 35, section="Customer Success"),
            FieldConfig("totango_customer_health", "Totango Customer Health", "picklist", False, False, 36,
                       ["Excellent", "Good", "Average", "Poor", "Critical"], "Customer Success"),
        ]
        
        account_records = [
            {
                # Account Information - matching the screenshot data
                "account_name": "Steed Standard Transport Ltd.",
                "enterprise_account_number": "16484517",
                "division": "PeopleNet/TMW CAD",
                "type": "Customer",
                "account_status_tmw": "CUSTOMER-(C) Live Customer",
                "tags": "",
                "lead_source": "",
                "trimble_tms_customer": False,
                "global_id": "G1005495",
                "customer_profile": "",
                "account_stage_tmw_us": "",
                "account_stage_tmw_aud": "",
                "customer_id_tmw_us": "",
                "customer_id_tmw_cad": "Steed Standard Transport - TMWCAN",
                "customer_id_tmw_aud": "",
                "parent_or_child_account": "Parent",
                "account_timezone": "Eastern Standard Time",
                "phone_tmw": "(519) 271-9924 x230",
                "fax_tmw": "",
                "website": "http://www.ssl.ca/",
                "lead_source_detail": "",
                "support_maintenance": "18%",
                "customer_drive_link": "",
                "account_stage_tmw_cad": "Customer",
                
                # Parent Hierarchy
                "parent_account_tmw_us": "",
                "parent_account_tmw_cad": "",
                "parent_account": "",
                "parent_netsuite_id": "",
                
                # Customer Success
                "customer_sentiment": "Average",
                "enterprise_risk_status": "",
                "enterprise_risk_reason": "",
                "enterprise_atrisk_severity": "",
                "enterprise_product_atrisk": "",
                "segmentation_tier": "Tier 5 CS Engage",
                "at_risk_update": "",
                "totango_customer_health": "Poor"
            },
            {
                # Sample second record
                "account_name": "Global Transport Inc.",
                "enterprise_account_number": "16484518",
                "division": "PeopleNet/TMW US",
                "type": "Prospect",
                "account_status_tmw": "PROSPECT-(P) Prospect",
                "tags": "High Priority",
                "lead_source": "Web",
                "trimble_tms_customer": True,
                "global_id": "G1005496",
                "customer_profile": "Enterprise",
                "account_stage_tmw_us": "Qualified",
                "account_stage_tmw_aud": "",
                "customer_id_tmw_us": "GTI-US-001",
                "customer_id_tmw_cad": "",
                "customer_id_tmw_aud": "",
                "parent_or_child_account": "Parent",
                "account_timezone": "Central Standard Time",
                "phone_tmw": "(555) 123-4567",
                "fax_tmw": "(555) 123-4568",
                "website": "https://globaltransport.com",
                "lead_source_detail": "Inbound Marketing",
                "support_maintenance": "25%",
                "customer_drive_link": "https://drive.google.com/folder123",
                "account_stage_tmw_cad": "Prospect",
                
                # Parent Hierarchy
                "parent_account_tmw_us": "",
                "parent_account_tmw_cad": "",
                "parent_account": "",
                "parent_netsuite_id": "NS-GTI-001",
                
                # Customer Success
                "customer_sentiment": "Good",
                "enterprise_risk_status": "Green",
                "enterprise_risk_reason": "",
                "enterprise_atrisk_severity": "Low",
                "enterprise_product_atrisk": "",
                "segmentation_tier": "Tier 2 Enterprise",
                "at_risk_update": "2024-01-15",
                "totango_customer_health": "Good"
            }
        ]
        
        # Contact object  
        contact_fields = [
            FieldConfig("first_name", "First Name", "text", True, True, 1, section="Contact Information"),
            FieldConfig("last_name", "Last Name", "text", True, True, 2, section="Contact Information"), 
            FieldConfig("email", "Email", "email", True, False, 3, section="Contact Information"),
            FieldConfig("phone", "Phone", "phone", True, False, 4, section="Contact Information"),
            FieldConfig("title", "Title", "text", True, False, 5, section="Contact Information"),
            FieldConfig("department", "Department", "text", True, False, 6, section="Contact Information"),
            FieldConfig("lead_source", "Lead Source", "picklist", True, False, 7,
                       ["Web", "Phone", "Email", "Partner", "Referral"], "Contact Information"),
            FieldConfig("mailing_street", "Mailing Street", "textarea", False, False, 8, section="Address Information"),
            FieldConfig("mailing_city", "Mailing City", "text", False, False, 9, section="Address Information"),
            FieldConfig("birthdate", "Birthdate", "date", False, False, 10, section="Personal Information"),
        ]
        
        contact_records = [
            {
                "first_name": "John",
                "last_name": "Smith", 
                "email": "john.smith@acme.com",
                "phone": "(555) 123-4567",
                "title": "CEO",
                "department": "Executive",
                "lead_source": "Referral",
                "mailing_street": "123 Main St",
                "mailing_city": "San Francisco",
                "birthdate": "1975-03-15"
            },
            {
                "first_name": "Sarah",
                "last_name": "Johnson",
                "email": "sarah.j@globalind.com", 
                "phone": "(555) 987-6543",
                "title": "VP of Operations",
                "department": "Operations",
                "lead_source": "Web",
                "mailing_street": "456 Industrial Blvd",
                "mailing_city": "Chicago",
                "birthdate": "1982-07-22"
            }
        ]
        
        # Store objects in session state
        st.session_state.objects = {
            'Account': SalesforceObject('Account', 'Accounts', account_fields, account_records),
            'Contact': SalesforceObject('Contact', 'Contacts', contact_fields, contact_records)
        }
    
    def render_sidebar(self):
        """Render the sidebar with object selection and field configuration"""
        st.sidebar.title("🔧 Configuration")
        
        # Object selection
        st.sidebar.subheader("Select Object")
        current_object = st.sidebar.selectbox(
            "Choose Salesforce Object:",
            list(st.session_state.objects.keys()),
            key="object_selector"
        )
        
        if current_object != st.session_state.current_object:
            st.session_state.current_object = current_object
            st.rerun()
        
        # Field configuration section
        st.sidebar.subheader("Field Configuration")
        obj = st.session_state.objects[st.session_state.current_object]
        
        st.sidebar.write("**Show/Hide Fields by Section:**")
        
        # Group fields by section for better organization
        sections = {}
        for field in obj.fields:
            section = field.section
            if section not in sections:
                sections[section] = []
            sections[section].append(field)
        
        # Create expandable sections in sidebar
        for section_name, section_fields in sections.items():
            with st.sidebar.expander(f"📂 {section_name}", expanded=section_name == "Account Information"):
                for field in section_fields:
                    field_index = obj.fields.index(field)  # Get the actual index in the main list
                    
                    new_visible = st.checkbox(
                        f"{field.label}",
                        value=field.visible,
                        key=f"field_visible_{field.name}",
                        help=f"Toggle visibility of {field.label} field"
                    )
                    
                    # Update field visibility if changed
                    if new_visible != field.visible:
                        obj.fields[field_index].visible = new_visible
        
        # Field reordering section
        st.sidebar.subheader("Field Order")
        visible_fields = [f for f in obj.fields if f.visible]
        
        if visible_fields:
            st.sidebar.write("**Drag to reorder fields:**")
            field_labels = [f.label for f in visible_fields]
            
            # Note: For now we'll use a simple selectbox for reordering
            # In a full implementation, you'd use streamlit-sortables
            selected_field = st.sidebar.selectbox(
                "Move field:",
                field_labels,
                key="field_to_move"
            )
            
            if st.sidebar.button("Move Up", key="move_up"):
                self.move_field_up(selected_field)
                st.rerun()
                
            if st.sidebar.button("Move Down", key="move_down"):
                self.move_field_down(selected_field)
                st.rerun()
    
    def move_field_up(self, field_label: str):
        """Move a field up in the order"""
        obj = st.session_state.objects[st.session_state.current_object]
        
        for i, field in enumerate(obj.fields):
            if field.label == field_label and field.visible and i > 0:
                # Find the previous visible field
                for j in range(i-1, -1, -1):
                    if obj.fields[j].visible:
                        # Swap orders
                        obj.fields[i].order, obj.fields[j].order = obj.fields[j].order, obj.fields[i].order
                        break
                break
    
    def move_field_down(self, field_label: str):
        """Move a field down in the order"""
        obj = st.session_state.objects[st.session_state.current_object]
        
        for i, field in enumerate(obj.fields):
            if field.label == field_label and field.visible and i < len(obj.fields) - 1:
                # Find the next visible field
                for j in range(i+1, len(obj.fields)):
                    if obj.fields[j].visible:
                        # Swap orders
                        obj.fields[i].order, obj.fields[j].order = obj.fields[j].order, obj.fields[i].order
                        break
                break
    
    def render_main_content(self):
        """Render the main content area with records"""
        obj = st.session_state.objects[st.session_state.current_object]
        
        # Header
        st.markdown(f"""
        <div class="sf-header">
            <h1>☁️ Mock Salesforce - {obj.label}</h1>
            <p>Configure and manage your {obj.label} data</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Object header with record count
        st.markdown(f"""
        <div class="sf-object-header">
            <h3>{obj.label} ({len(obj.records)} records)</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Add new record button
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button(f"➕ New {obj.name}", type="primary"):
                self.create_new_record()
        
        # Records display
        visible_fields = sorted([f for f in obj.fields if f.visible], key=lambda x: x.order)
        
        if not visible_fields:
            st.warning("No fields are currently visible. Please enable some fields in the sidebar.")
            return
        
        # Display records as cards (more Salesforce-like)
        for i, record in enumerate(obj.records):
            self.render_record_card(record, visible_fields, i)
    
    def render_record_card(self, record: Dict[str, Any], visible_fields: List[FieldConfig], record_index: int):
        """Render a single record as a card with collapsible sections like Salesforce"""
        with st.container():
            st.markdown('<div class="field-container">', unsafe_allow_html=True)
            
            # Record header
            primary_field = visible_fields[0] if visible_fields else None
            header_value = record.get(primary_field.name, "Unnamed Record") if primary_field else "Unnamed Record"
            
            col1, col2 = st.columns([3, 1])
            with col1:
                st.subheader(f"📋 {header_value}")
            with col2:
                edit_key = f"edit_record_{record_index}"
                if st.button("✏️ Edit", key=edit_key):
                    st.session_state.editing_record = record_index
                    st.rerun()
            
            # Group fields by section
            sections = {}
            for field in visible_fields:
                section = field.section
                if section not in sections:
                    sections[section] = []
                sections[section].append(field)
            
            # Display each section as an expandable area
            for section_name, section_fields in sections.items():
                with st.expander(f"📂 {section_name}", expanded=True):
                    # Display fields in a 2-column grid (like Salesforce)
                    cols = st.columns(2)
                    
                    for i, field in enumerate(section_fields):
                        col_idx = i % 2
                        with cols[col_idx]:
                            value = record.get(field.name, "")
                            
                            # Format value based on field type
                            formatted_value = self.format_field_value(value, field.field_type)
                            
                            # Add edit icon for editable fields (like in Salesforce)
                            edit_icon = "✏️" if not field.required else ""
                            
                            st.markdown(f"""
                            <div class="field-label">{field.label} {edit_icon}</div>
                            <div>{formatted_value}</div>
                            """, unsafe_allow_html=True)
                            st.markdown("<br/>", unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown("---")
    
    def format_field_value(self, value: Any, field_type: str) -> str:
        """Format a field value based on its type"""
        if value is None or value == "":
            return "<em>--</em>"
        
        if field_type == "currency":
            return f"${value:,.2f}" if isinstance(value, (int, float)) else str(value)
        elif field_type == "number":
            return f"{value:,}" if isinstance(value, (int, float)) else str(value)
        elif field_type == "percentage":
            return str(value) if isinstance(value, str) and value.endswith("%") else f"{value}%"
        elif field_type == "checkbox":
            return "✅ Yes" if value else "❌ No"
        elif field_type == "date":
            return str(value)
        elif field_type == "email":
            return f'<a href="mailto:{value}">{value}</a>'
        elif field_type == "phone":
            return f'<a href="tel:{value}">{value}</a>'
        elif field_type == "url":
            return f'<a href="{value}" target="_blank">{value}</a>'
        else:
            return str(value)
    
    def create_new_record(self):
        """Handle creating a new record"""
        st.session_state.editing_record = -1  # -1 indicates new record
        st.rerun()
    
    def render_edit_modal(self):
        """Render the edit/create record modal"""
        if st.session_state.editing_record is None:
            return
        
        obj = st.session_state.objects[st.session_state.current_object]
        is_new_record = st.session_state.editing_record == -1
        
        # Modal header
        modal_title = f"Create New {obj.name}" if is_new_record else f"Edit {obj.name}"
        st.subheader(modal_title)
        
        # Get current record data or create empty record
        if is_new_record:
            record_data = {}
        else:
            record_data = obj.records[st.session_state.editing_record].copy()
        
        # Create form for editing
        with st.form(key="edit_record_form"):
            visible_fields = sorted([f for f in obj.fields if f.visible], key=lambda x: x.order)
            
            # Create input fields based on field types, organized by section
            updated_data = {}
            
            # Group fields by section for better form organization
            sections = {}
            for field in visible_fields:
                section = field.section
                if section not in sections:
                    sections[section] = []
                sections[section].append(field)
            
            # Display form fields organized by section
            for section_name, section_fields in sections.items():
                st.subheader(f"📂 {section_name}")
                
                for field in section_fields:
                    current_value = record_data.get(field.name, "")
                    
                    if field.field_type == "text":
                        updated_data[field.name] = st.text_input(
                            field.label,
                            value=current_value,
                            key=f"edit_{field.name}",
                            help=f"Enter {field.label.lower()}"
                        )
                    elif field.field_type == "textarea":
                        updated_data[field.name] = st.text_area(
                            field.label,
                            value=current_value,
                            key=f"edit_{field.name}",
                            height=100
                        )
                    elif field.field_type == "email":
                        updated_data[field.name] = st.text_input(
                            field.label,
                            value=current_value,
                            key=f"edit_{field.name}",
                            help="Enter a valid email address"
                        )
                    elif field.field_type == "phone":
                        updated_data[field.name] = st.text_input(
                            field.label,
                            value=current_value,
                            key=f"edit_{field.name}",
                            help="Enter phone number"
                        )
                    elif field.field_type == "checkbox":
                        updated_data[field.name] = st.checkbox(
                            field.label,
                            value=bool(current_value),
                            key=f"edit_{field.name}",
                            help=f"Check to enable {field.label.lower()}"
                        )
                    elif field.field_type == "percentage":
                        # Handle percentage field (could be text with % or just number)
                        percent_value = current_value
                        if isinstance(current_value, str) and current_value.endswith("%"):
                            percent_value = current_value.rstrip("%")
                        
                        updated_data[field.name] = st.text_input(
                            field.label,
                            value=percent_value,
                            key=f"edit_{field.name}",
                            help="Enter percentage value (% will be added automatically)"
                        )
                    elif field.field_type == "picklist":
                        current_index = 0
                        if current_value and current_value in field.options:
                            current_index = field.options.index(current_value)
                        
                        updated_data[field.name] = st.selectbox(
                            field.label,
                            field.options,
                            index=current_index,
                            key=f"edit_{field.name}"
                        )
                    elif field.field_type == "number":
                        updated_data[field.name] = st.number_input(
                            field.label,
                            value=int(current_value) if current_value and str(current_value).isdigit() else 0,
                            key=f"edit_{field.name}"
                        )
                    elif field.field_type == "currency":
                        updated_data[field.name] = st.number_input(
                            field.label,
                            value=float(current_value) if current_value else 0.0,
                            format="%.2f",
                            key=f"edit_{field.name}"
                        )
                    elif field.field_type == "date":
                        try:
                            date_value = datetime.strptime(current_value, "%Y-%m-%d").date() if current_value else date.today()
                        except:
                            date_value = date.today()
                        
                        updated_data[field.name] = st.date_input(
                            field.label,
                            value=date_value,
                            key=f"edit_{field.name}"
                        )
                    elif field.field_type == "url":
                        updated_data[field.name] = st.text_input(
                            field.label,
                            value=current_value,
                            key=f"edit_{field.name}",
                            help="Enter a valid URL (include http:// or https://)"
                        )
            
            # Form buttons
            col1, col2, col3 = st.columns([1, 1, 2])
            
            with col1:
                if st.form_submit_button("💾 Save", type="primary"):
                    self.save_record(updated_data, is_new_record)
                    st.session_state.editing_record = None
                    st.success("Record saved successfully!")
                    st.rerun()
            
            with col2:
                if st.form_submit_button("❌ Cancel"):
                    st.session_state.editing_record = None
                    st.rerun()
            
            # Delete button for existing records
            if not is_new_record:
                with col3:
                    if st.form_submit_button("🗑️ Delete", type="secondary"):
                        self.delete_record(st.session_state.editing_record)
                        st.session_state.editing_record = None
                        st.success("Record deleted successfully!")
                        st.rerun()
    
    def save_record(self, record_data: Dict[str, Any], is_new_record: bool):
        """Save a record (create new or update existing)"""
        obj = st.session_state.objects[st.session_state.current_object]
        
        # Convert date objects to strings for JSON serialization
        for key, value in record_data.items():
            if isinstance(value, date):
                record_data[key] = value.strftime("%Y-%m-%d")
        
        if is_new_record:
            obj.records.append(record_data)
        else:
            obj.records[st.session_state.editing_record] = record_data
    
    def delete_record(self, record_index: int):
        """Delete a record"""
        obj = st.session_state.objects[st.session_state.current_object]
        if 0 <= record_index < len(obj.records):
            del obj.records[record_index]
    
    def run(self):
        """Main application runner"""
        # Render sidebar
        self.render_sidebar()
        
        # Render main content
        self.render_main_content()
        
        # Render edit modal if active
        if st.session_state.editing_record is not None:
            st.markdown("---")
            self.render_edit_modal()
        
        # Footer
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; color: #666; padding: 2rem;">
            <p>🚀 Mock Salesforce App - Built with Streamlit</p>
            <p><em>Configure fields using the sidebar • Add/Edit records • Share with your team</em></p>
        </div>
        """, unsafe_allow_html=True)

# Run the application
if __name__ == "__main__":
    app = MockSalesforceApp()
    app.run()
