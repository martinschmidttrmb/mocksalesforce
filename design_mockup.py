"""
Salesforce Design Mockup Tool
============================
A simple tool for creating visual mockups of Salesforce pages.
Focus: Design and layout, not functionality.

Author: Assistant for Vibe Coder
"""

import streamlit as st
import json
from typing import Dict, List
from dataclasses import dataclass, asdict

# Page configuration
st.set_page_config(
    page_title="Salesforce Design Mockup",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Salesforce-like styling
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
    }
    
    .sf-field-grid {
        padding: 1rem;
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem;
    }
    
    .sf-field {
        margin-bottom: 1rem;
    }
    
    .sf-field-label {
        font-weight: 600;
        color: #3E3E3C;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.025rem;
        margin-bottom: 0.25rem;
    }
    
    .sf-field-value {
        color: #080707;
        font-size: 0.875rem;
        padding: 0.5rem 0;
        border-bottom: 1px solid #E5E5E5;
    }
    
    .field-moveable {
        background-color: #F8F9FA;
        border: 1px solid #DEE2E6;
        border-radius: 0.25rem;
        padding: 0.5rem;
        margin: 0.25rem 0;
        cursor: move;
        transition: all 0.2s;
    }
    
    .field-moveable:hover {
        background-color: #E9ECEF;
        border-color: #1B96FF;
    }
    
    .section-moveable {
        border-left: 4px solid #1B96FF;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

@dataclass
class MockField:
    """A field in the mockup"""
    name: str
    label: str
    value: str = "--"
    field_type: str = "text"
    visible: bool = True

@dataclass
class MockSection:
    """A section containing fields"""
    name: str
    title: str
    fields: List[MockField]
    expanded: bool = True
    visible: bool = True

class SalesforceDesignMockup:
    """Main class for the Salesforce design mockup tool"""
    
    def __init__(self):
        self.init_session_state()
        self.load_sample_design()
    
    def init_session_state(self):
        """Initialize session state variables"""
        if 'current_design' not in st.session_state:
            st.session_state.current_design = "Account Page"
        
        if 'designs' not in st.session_state:
            st.session_state.designs = {}
            
        if 'preview_mode' not in st.session_state:
            st.session_state.preview_mode = False
    
    def load_sample_design(self):
        """Load the sample Account design based on your screenshot"""
        if 'Account Page' not in st.session_state.designs:
            # Account Information Section
            account_info_fields = [
                MockField("account_name", "Account Name", "Steed Standard Transport Ltd."),
                MockField("enterprise_account", "Enterprise Account Number", "16484517"),
                MockField("division", "Division", "PeopleNet/TMW CAD"),
                MockField("type", "Type", "Customer"),
                MockField("account_status", "Account Status TMW", "CUSTOMER-(C) Live Customer"),
                MockField("tags", "Tags", ""),
                MockField("lead_source", "Lead Source", ""),
                MockField("trimble_customer", "Trimble TMS Customer", "☐"),
                MockField("global_id", "Global ID", "G1005495"),
                MockField("customer_profile", "Customer Profile", ""),
                MockField("account_stage_us", "Account Stage TMW US", ""),
                MockField("account_stage_aud", "Account Stage TMW AUD", ""),
                MockField("customer_id_us", "Customer Id TMW US", ""),
                MockField("customer_id_cad", "Customer Id TMW CAD", "Steed Standard Transport - TMWCAN"),
                MockField("customer_id_aud", "Customer Id TMW AUD", ""),
                MockField("parent_child", "Parent or Child Account", "Parent"),
                MockField("timezone", "Account Time Zone (US & CA)", "Eastern Standard Time"),
                MockField("phone", "Phone TMW", "(519) 271-9924 x230"),
                MockField("fax", "Fax TMW", ""),
                MockField("website", "Website", "http://www.ssl.ca/"),
                MockField("lead_source_detail", "Lead Source Detail", ""),
                MockField("support_maintenance", "Support & Maintenance", "18%"),
                MockField("drive_link", "Customer Drive Link", ""),
                MockField("account_stage_cad", "Account Stage TMW CAD", "Customer"),
            ]
            
            # Parent Hierarchy Section
            parent_fields = [
                MockField("parent_us", "Parent Account TMW US", ""),
                MockField("parent_cad", "Parent Account TMW CAD", ""),
                MockField("parent_account", "Parent Account", ""),
                MockField("parent_netsuite", "Parent NetSuite Id", ""),
            ]
            
            # Customer Success Section
            success_fields = [
                MockField("sentiment", "Customer Sentiment", "Average"),
                MockField("risk_status", "Enterprise Risk Status", ""),
                MockField("risk_reason", "Enterprise Risk Reason", ""),
                MockField("risk_severity", "Enterprise At-Risk Severity Level", ""),
                MockField("product_risk", "Enterprise Product At Risk", ""),
                MockField("segmentation", "Segmentation Tier", "Tier 5 CS Engage"),
                MockField("risk_update", "At Risk Update", ""),
                MockField("totango_health", "Totango Customer Health", "Poor"),
            ]
            
            # Create sections
            sections = [
                MockSection("account_info", "Account Information", account_info_fields, True, True),
                MockSection("parent_hierarchy", "Parent Hierarchy", parent_fields, True, True),
                MockSection("customer_success", "Customer Success", success_fields, True, True)
            ]
            
            st.session_state.designs["Account Page"] = sections
    
    def render_sidebar(self):
        """Render the design configuration sidebar"""
        st.sidebar.title("🎨 Design Controls")
        
        # Design selector
        st.sidebar.subheader("Current Design")
        designs = list(st.session_state.designs.keys())
        current = st.sidebar.selectbox("Select Design:", designs, key="design_selector")
        
        if current != st.session_state.current_design:
            st.session_state.current_design = current
            st.rerun()
        
        # Preview mode toggle
        st.sidebar.subheader("Display Mode")
        preview = st.sidebar.checkbox("👁️ Preview Mode", st.session_state.preview_mode)
        if preview != st.session_state.preview_mode:
            st.session_state.preview_mode = preview
            st.rerun()
        
        if not st.session_state.preview_mode:
            st.sidebar.markdown("---")
            self.render_section_controls()
            st.sidebar.markdown("---")
            self.render_field_controls()
            st.sidebar.markdown("---")
            self.render_design_tools()
    
    def render_section_controls(self):
        """Render section management controls"""
        st.sidebar.subheader("📂 Sections")
        
        sections = st.session_state.designs[st.session_state.current_design]
        
        for i, section in enumerate(sections):
            col1, col2, col3, col4 = st.sidebar.columns([1, 2, 1, 1])
            
            with col1:
                visible = st.checkbox("", section.visible, key=f"sec_vis_{i}")
                if visible != section.visible:
                    sections[i].visible = visible
            
            with col2:
                st.write(f"**{section.title}**")
            
            with col3:
                if st.button("↑", key=f"sec_up_{i}", disabled=i==0):
                    sections[i], sections[i-1] = sections[i-1], sections[i]
                    st.rerun()
            
            with col4:
                if st.button("↓", key=f"sec_down_{i}", disabled=i==len(sections)-1):
                    sections[i], sections[i+1] = sections[i+1], sections[i]
                    st.rerun()
        
        # Add new section
        if st.sidebar.button("➕ Add Section"):
            new_section = MockSection(f"section_{len(sections)}", "New Section", [], True, True)
            sections.append(new_section)
            st.rerun()
    
    def render_field_controls(self):
        """Render field management controls"""
        st.sidebar.subheader("🏷️ Fields")
        
        sections = st.session_state.designs[st.session_state.current_design]
        selected_section = st.sidebar.selectbox("Edit Section Fields:", 
                                               [s.title for s in sections if s.visible])
        
        if selected_section:
            section = next(s for s in sections if s.title == selected_section)
            
            for i, field in enumerate(section.fields):
                with st.sidebar.expander(f"{field.label}", expanded=False):
                    # Field visibility
                    field.visible = st.checkbox("Visible", field.visible, key=f"field_vis_{section.name}_{i}")
                    
                    # Field label
                    field.label = st.text_input("Label:", field.label, key=f"field_label_{section.name}_{i}")
                    
                    # Field value
                    field.value = st.text_input("Sample Value:", field.value, key=f"field_value_{section.name}_{i}")
                    
                    # Field movement
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.button("↑", key=f"field_up_{section.name}_{i}", disabled=i==0):
                            section.fields[i], section.fields[i-1] = section.fields[i-1], section.fields[i]
                            st.rerun()
                    with col2:
                        if st.button("↓", key=f"field_down_{section.name}_{i}", disabled=i==len(section.fields)-1):
                            section.fields[i], section.fields[i+1] = section.fields[i+1], section.fields[i]
                            st.rerun()
                    with col3:
                        if st.button("🗑️", key=f"field_delete_{section.name}_{i}"):
                            section.fields.pop(i)
                            st.rerun()
            
            # Add new field
            if st.sidebar.button(f"➕ Add Field to {selected_section}"):
                new_field = MockField(f"field_{len(section.fields)}", "New Field", "Sample Value")
                section.fields.append(new_field)
                st.rerun()
    
    def render_design_tools(self):
        """Render design and export tools"""
        st.sidebar.subheader("🛠️ Design Tools")
        
        # Save design
        if st.sidebar.button("💾 Save Design"):
            st.sidebar.success("Design saved!")
        
        # Export design
        if st.sidebar.button("📤 Export Design"):
            design_data = st.session_state.designs[st.session_state.current_design]
            design_json = json.dumps([asdict(section) for section in design_data], indent=2)
            st.sidebar.download_button(
                "Download JSON",
                design_json,
                f"{st.session_state.current_design.lower().replace(' ', '_')}_design.json",
                "application/json"
            )
        
        # Create new design
        st.sidebar.text_input("New Design Name:", placeholder="Enter name...", key="new_design_name")
        if st.sidebar.button("🆕 Create New Design"):
            name = st.session_state.get("new_design_name", "")
            if name and name not in st.session_state.designs:
                st.session_state.designs[name] = [
                    MockSection("section_1", "New Section", [
                        MockField("field_1", "Sample Field", "Sample Value")
                    ])
                ]
                st.session_state.current_design = name
                st.rerun()
    
    def render_main_design(self):
        """Render the main design preview"""
        sections = st.session_state.designs[st.session_state.current_design]
        
        # Header
        st.markdown(f"""
        <div class="sf-header">
            <h1>☁️ Salesforce - {st.session_state.current_design}</h1>
            <p>{'Preview Mode' if st.session_state.preview_mode else 'Design Mode - Use sidebar to modify layout'}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Render sections
        for section in sections:
            if section.visible:
                self.render_section(section)
    
    def render_section(self, section: MockSection):
        """Render a single section"""
        st.markdown(f"""
        <div class="sf-section {'section-moveable' if not st.session_state.preview_mode else ''}">
            <div class="sf-section-header">
                {'📂' if section.expanded else '📁'} {section.title}
                {f' ({len([f for f in section.fields if f.visible])} fields)' if not st.session_state.preview_mode else ''}
            </div>
            <div class="sf-field-grid">
        """, unsafe_allow_html=True)
        
        visible_fields = [f for f in section.fields if f.visible]
        
        # Display fields in two-column grid
        for i, field in enumerate(visible_fields):
            # Add visual indicators in design mode
            field_class = "field-moveable" if not st.session_state.preview_mode else ""
            drag_indicator = "⋮⋮ " if not st.session_state.preview_mode else ""
            
            st.markdown(f"""
                <div class="sf-field {field_class}">
                    <div class="sf-field-label">{drag_indicator}{field.label}</div>
                    <div class="sf-field-value">{field.value if field.value else '--'}</div>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div></div>", unsafe_allow_html=True)
    
    def run(self):
        """Main application runner"""
        # Render sidebar
        self.render_sidebar()
        
        # Render main design
        self.render_main_design()
        
        # Instructions footer
        if not st.session_state.preview_mode:
            st.markdown("---")
            st.markdown("""
            <div style="text-align: center; color: #666; padding: 1rem;">
                <p>🎨 <strong>Design Mode</strong> - Use the sidebar to:</p>
                <p>📂 Show/hide and reorder sections • 🏷️ Edit field labels and values • ⋮⋮ Move fields around</p>
                <p>👁️ Toggle <strong>Preview Mode</strong> to see the clean final result</p>
            </div>
            """, unsafe_allow_html=True)

# Run the application
if __name__ == "__main__":
    app = SalesforceDesignMockup()
    app.run()
