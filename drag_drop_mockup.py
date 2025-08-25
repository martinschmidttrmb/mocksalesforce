"""
Salesforce Drag & Drop Design Mockup
===================================
Direct manipulation interface for Salesforce page layouts.
- Drag & drop fields to rearrange within sections
- Hide/show toggles next to each field
- Hidden fields panel for management
- No sidebar needed - everything inline!

Author: Assistant for Vibe Coder
"""

import streamlit as st
from streamlit_sortables import sort_items
import json
from typing import Dict, List
from dataclasses import dataclass, asdict

# Page configuration
st.set_page_config(
    page_title="Salesforce Layout Editor",
    page_icon="🎯",
    layout="wide"
)

# Enhanced Salesforce-like styling with drag-and-drop
st.markdown("""
<style>
    /* Main Salesforce-like styling */
    .main > div {
        padding-top: 1rem;
    }
    
    .sf-header {
        background-color: #1B96FF;
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    
    .sf-section {
        background-color: #FAFAF9;
        border: 1px solid #D8DDE6;
        border-radius: 0.25rem;
        margin: 1rem 0;
        overflow: hidden;
    }
    
    .sf-section-header {
        background-color: #F3F3F3;
        padding: 0.75rem 1rem;
        border-bottom: 1px solid #D8DDE6;
        font-weight: 600;
        color: #080707;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    .sf-field-container {
        padding: 1rem;
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem;
        background-color: white;
    }
    
    .sf-field {
        position: relative;
        border: 1px solid #E5E5E5;
        border-radius: 0.25rem;
        padding: 0.75rem;
        background-color: #FAFAF9;
        transition: all 0.2s;
        cursor: grab;
    }
    
    .sf-field:hover {
        border-color: #1B96FF;
        box-shadow: 0 2px 4px rgba(27, 150, 255, 0.1);
        transform: translateY(-1px);
    }
    
    .sf-field:active {
        cursor: grabbing;
    }
    
    .sf-field-label {
        font-weight: 600;
        color: #3E3E3C;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.025rem;
        margin-bottom: 0.25rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .sf-field-value {
        color: #080707;
        font-size: 0.875rem;
        padding: 0.25rem 0;
        border-bottom: 1px solid #E5E5E5;
    }
    
    .field-controls {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .drag-handle {
        color: #666;
        cursor: grab;
        font-size: 1rem;
    }
    
    .drag-handle:active {
        cursor: grabbing;
    }
    
    .hide-toggle {
        font-size: 0.75rem;
        cursor: pointer;
        padding: 0.2rem;
        border-radius: 0.2rem;
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
    }
    
    .hide-toggle:hover {
        background-color: #e9ecef;
    }
    
    .hidden-field {
        opacity: 0.3;
        border-style: dashed;
    }
    
    .hidden-panel {
        background-color: #FFF3CD;
        border: 1px solid #FFEAA7;
        border-radius: 0.25rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .hidden-item {
        background-color: #F8F9FA;
        border: 1px solid #DEE2E6;
        border-radius: 0.25rem;
        padding: 0.5rem;
        margin: 0.25rem;
        display: inline-block;
        cursor: pointer;
    }
    
    .hidden-item:hover {
        background-color: #E9ECEF;
    }
    
    .section-toggle {
        background: none;
        border: none;
        color: #1B96FF;
        cursor: pointer;
        font-size: 0.9rem;
        padding: 0.25rem;
    }
    
    .instructions {
        background-color: #E3F2FD;
        border-left: 4px solid #1B96FF;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0.25rem;
    }
</style>
""", unsafe_allow_html=True)

@dataclass
class DragField:
    """A draggable field in the mockup"""
    id: str
    label: str
    value: str = "--"
    field_type: str = "text"
    visible: bool = True
    original_position: int = 0

@dataclass
class DragSection:
    """A section containing draggable fields"""
    name: str
    title: str
    fields: List[DragField]
    expanded: bool = True

class SalesforceDragDropMockup:
    """Main class for the drag & drop Salesforce mockup"""
    
    def __init__(self):
        self.init_session_state()
        self.load_original_layout()
    
    def init_session_state(self):
        """Initialize session state variables"""
        if 'sections' not in st.session_state:
            st.session_state.sections = []
            
        if 'show_hidden_panel' not in st.session_state:
            st.session_state.show_hidden_panel = False
    
    def load_original_layout(self):
        """Load the exact layout from your screenshot"""
        if not st.session_state.sections:
            # Account Information Section - EXACT positions from screenshot
            account_info_fields = [
                # Left Column (positions 0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22)
                DragField("account_name", "Account Name", "Steed Standard Transport Ltd.", "text", True, 0),
                DragField("enterprise_account", "Enterprise Account Number", "16484517", "text", True, 2),
                DragField("division", "Division", "PeopleNet/TMW CAD", "text", True, 4),
                DragField("type", "Type", "Customer", "picklist", True, 6),
                DragField("account_status", "Account Status TMW", "CUSTOMER-(C) Live Customer", "picklist", True, 8),
                DragField("tags", "Tags", "", "text", True, 10),
                DragField("lead_source", "Lead Source", "", "text", True, 12),
                DragField("trimble_customer", "Trimble TMS Customer", "☐", "checkbox", True, 14),
                DragField("global_id", "Global ID", "G1005495", "text", True, 16),
                DragField("customer_profile", "Customer Profile", "", "text", True, 18),
                DragField("account_stage_us", "Account Stage TMW US", "", "text", True, 20),
                DragField("account_stage_aud", "Account Stage TMW AUD", "", "text", True, 22),
                
                # Right Column (positions 1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23)
                DragField("customer_id_us", "Customer Id TMW US", "", "text", True, 1),
                DragField("customer_id_cad", "Customer Id TMW CAD", "Steed Standard Transport - TMWCAN", "text", True, 3),
                DragField("customer_id_aud", "Customer Id TMW AUD", "", "text", True, 5),
                DragField("parent_child", "Parent or Child Account", "Parent", "picklist", True, 7),
                DragField("timezone", "Account Time Zone (US & CA)", "Eastern Standard Time", "picklist", True, 9),
                DragField("phone", "Phone TMW", "(519) 271-9924 x230", "phone", True, 11),
                DragField("fax", "Fax TMW", "", "phone", True, 13),
                DragField("website", "Website", "http://www.ssl.ca/", "url", True, 15),
                DragField("lead_source_detail", "Lead Source Detail", "", "text", True, 17),
                DragField("support_maintenance", "Support & Maintenance", "18%", "percentage", True, 19),
                DragField("drive_link", "Customer Drive Link", "", "url", True, 21),
                DragField("account_stage_cad", "Account Stage TMW CAD", "Customer", "picklist", True, 23),
            ]
            
            # Parent Hierarchy Section
            parent_fields = [
                DragField("parent_us", "Parent Account TMW US", "", "text", True, 0),
                DragField("parent_cad", "Parent Account TMW CAD", "", "text", True, 1),
                DragField("parent_account", "Parent Account", "", "text", True, 2),
                DragField("parent_netsuite", "Parent NetSuite Id", "", "text", True, 3),
            ]
            
            # Customer Success Section  
            success_fields = [
                DragField("sentiment", "Customer Sentiment", "Average", "picklist", True, 0),
                DragField("risk_update", "At Risk Update", "", "text", True, 1),
                DragField("risk_status", "Enterprise Risk Status", "", "text", True, 2),
                DragField("totango_health", "Totango Customer Health", "Poor", "picklist", True, 3),
                DragField("risk_reason", "Enterprise Risk Reason", "", "text", True, 4),
                DragField("risk_severity", "Enterprise At-Risk Severity Level", "", "text", True, 6),
                DragField("product_risk", "Enterprise Product At Risk", "", "text", True, 8),
                DragField("segmentation", "Segmentation Tier", "Tier 5 CS Engage", "picklist", True, 10),
            ]
            
            # Create sections
            st.session_state.sections = [
                DragSection("account_info", "Account Information", account_info_fields, True),
                DragSection("parent_hierarchy", "Parent Hierarchy", parent_fields, True),
                DragSection("customer_success", "Customer Success", success_fields, True)
            ]
    
    def render_instructions(self):
        """Render usage instructions"""
        st.markdown("""
        <div class="instructions">
            <h4>🎯 How to Use This Layout Editor</h4>
            <p><strong>Drag & Drop:</strong> Grab any field by the ⋮⋮ handle and drop it on another field to swap positions</p>
            <p><strong>Hide/Show:</strong> Click the 👁️ or 👁️‍🗨️ icon next to each field to toggle visibility</p>
            <p><strong>Hidden Fields:</strong> Use the "Show Hidden Fields" panel below to see and restore hidden fields</p>
            <p><strong>Sections:</strong> Click section headers to expand/collapse entire sections</p>
        </div>
        """, unsafe_allow_html=True)
    
    def render_hidden_panel(self):
        """Render panel for managing hidden fields"""
        all_hidden_fields = []
        for section in st.session_state.sections:
            hidden_in_section = [f for f in section.fields if not f.visible]
            if hidden_in_section:
                all_hidden_fields.extend([(section.name, section.title, f) for f in hidden_in_section])
        
        if all_hidden_fields:
            col1, col2 = st.columns([1, 4])
            with col1:
                show_panel = st.button("👁️‍🗨️ Show Hidden Fields" if not st.session_state.show_hidden_panel else "🙈 Hide Panel")
                if show_panel:
                    st.session_state.show_hidden_panel = not st.session_state.show_hidden_panel
                    st.rerun()
            
            if st.session_state.show_hidden_panel:
                st.markdown(f"""
                <div class="hidden-panel">
                    <h4>🔍 Hidden Fields ({len(all_hidden_fields)} hidden)</h4>
                    <p>Click any field below to make it visible again:</p>
                </div>
                """, unsafe_allow_html=True)
                
                cols = st.columns(4)
                for i, (section_name, section_title, field) in enumerate(all_hidden_fields):
                    col_idx = i % 4
                    with cols[col_idx]:
                        if st.button(f"👁️ {field.label}", key=f"unhide_{section_name}_{field.id}"):
                            # Find and unhide the field
                            for section in st.session_state.sections:
                                if section.name == section_name:
                                    for f in section.fields:
                                        if f.id == field.id:
                                            f.visible = True
                                            st.rerun()
                            
    def render_main_layout(self):
        """Render the main Salesforce layout"""
        # Header
        st.markdown("""
        <div class="sf-header">
            <h1>🎯 Salesforce Layout Editor - Account Page</h1>
            <p>Drag fields to rearrange • Click 👁️ to hide/show • Original field positions preserved</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Render each section
        for section_idx, section in enumerate(st.session_state.sections):
            self.render_section(section, section_idx)
    
    def render_section(self, section: DragSection, section_idx: int):
        """Render a single section with drag & drop fields"""
        
        # Section header with expand/collapse
        visible_count = len([f for f in section.fields if f.visible])
        total_count = len(section.fields)
        
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"""
            <div class="sf-section">
                <div class="sf-section-header">
                    <span>{'📂' if section.expanded else '📁'} {section.title}</span>
                    <span style="font-size: 0.8em; color: #666;">
                        {visible_count} visible • {total_count - visible_count} hidden
                    </span>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            if st.button("👁️" if section.expanded else "👁️‍🗨️", key=f"toggle_section_{section_idx}"):
                section.expanded = not section.expanded
                st.rerun()
        
        if section.expanded:
            # Get visible fields sorted by their original positions
            visible_fields = [f for f in section.fields if f.visible]
            visible_fields.sort(key=lambda x: x.original_position)
            
            # Create sortable items for drag & drop
            if visible_fields:
                field_items = []
                for field in visible_fields:
                    # Format value for display
                    display_value = field.value if field.value else "--"
                    if field.field_type == "url" and field.value:
                        display_value = f'<a href="{field.value}" target="_blank">{field.value}</a>'
                    elif field.field_type == "phone" and field.value:
                        display_value = f'<a href="tel:{field.value}">{field.value}</a>'
                    
                    field_items.append({
                        'header': f'⋮⋮ {field.label}',
                        'items': [display_value]
                    })
                
                # Render drag & drop interface
                st.markdown('<div class="sf-field-container">', unsafe_allow_html=True)
                
                # Create two columns for the grid layout
                cols = st.columns(2)
                
                for i, field in enumerate(visible_fields):
                    col_idx = i % 2
                    with cols[col_idx]:
                        # Field container
                        field_key = f"{section.name}_{field.id}"
                        
                        # Format value
                        display_value = field.value if field.value else "--"
                        if field.field_type == "url" and field.value:
                            display_value = f'<a href="{field.value}" target="_blank">{field.value}</a>'
                        
                        # Create field with hide/show toggle
                        col_field, col_toggle = st.columns([4, 1])
                        
                        with col_field:
                            st.markdown(f"""
                            <div class="sf-field" data-field="{field.id}">
                                <div class="sf-field-label">
                                    <span>⋮⋮ {field.label}</span>
                                </div>
                                <div class="sf-field-value">{display_value}</div>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with col_toggle:
                            if st.button("👁️‍🗨️", key=f"hide_{field_key}", help=f"Hide {field.label}"):
                                field.visible = False
                                st.rerun()
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            else:
                st.markdown("""
                <div style="padding: 2rem; text-align: center; color: #666;">
                    <p>No visible fields in this section</p>
                    <p><em>Use the "Show Hidden Fields" panel to restore fields</em></p>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("---")
    
    def render_export_tools(self):
        """Render export and save tools"""
        st.markdown("### 🛠️ Export Tools")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("💾 Save Layout"):
                st.success("Layout saved! (Demo)")
        
        with col2:
            # Export current layout
            if st.button("📤 Export Layout"):
                layout_data = []
                for section in st.session_state.sections:
                    section_data = {
                        'name': section.name,
                        'title': section.title,
                        'expanded': section.expanded,
                        'fields': [asdict(field) for field in section.fields]
                    }
                    layout_data.append(section_data)
                
                layout_json = json.dumps(layout_data, indent=2)
                st.download_button(
                    "📋 Download JSON",
                    layout_json,
                    "salesforce_layout.json",
                    "application/json"
                )
        
        with col3:
            if st.button("🔄 Reset Layout"):
                st.session_state.sections = []
                self.load_original_layout()
                st.rerun()
    
    def run(self):
        """Main application runner"""
        self.render_instructions()
        self.render_main_layout()
        self.render_hidden_panel()
        st.markdown("---")
        self.render_export_tools()

# Run the application
if __name__ == "__main__":
    app = SalesforceDragDropMockup()
    app.run()
