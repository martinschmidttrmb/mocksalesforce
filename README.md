# Mock Salesforce App 🚀

A beautiful Streamlit-based mock Salesforce interface that allows you to prototype and share Salesforce configurations with your team!

## 🌟 Features

- **Object Management**: Work with different Salesforce objects (Account, Contact, and more)
- **Field Configuration**: Show/hide fields and reorder them easily
- **Data Management**: Add, edit, and delete records just like in Salesforce  
- **Team Sharing**: Share your configurations with team members
- **Salesforce-like UI**: Familiar interface that matches Salesforce styling

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the App

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 🎯 How to Use

### Configuring Fields
1. **Select Object**: Use the sidebar to choose between Account, Contact, or other objects
2. **Show/Hide Fields**: Check/uncheck fields in the "Field Configuration" section
3. **Reorder Fields**: Use the "Move Up/Down" buttons to reorder visible fields

### Managing Records
1. **View Records**: All records are displayed as cards in the main area
2. **Add New Record**: Click the "➕ New [Object]" button
3. **Edit Record**: Click the "✏️ Edit" button on any record card
4. **Delete Record**: Use the delete button when editing a record

### Adding Screenshots
When you provide screenshots of your actual Salesforce setup:
1. The app can be easily modified to match your exact field layouts
2. New objects can be added with their specific fields
3. Field types and validation can be customized

## 🔧 Customization

The app is designed to be easily customizable:

- **Add New Objects**: Modify the `load_default_objects()` method in `app.py`
- **New Field Types**: Add support for additional Salesforce field types
- **Custom Styling**: Update the CSS in the `st.markdown()` sections
- **Data Import**: Load real data from CSV files or APIs

## 📱 Sharing with Team

To share with your team:
1. **Local Network**: Others can access via your IP address (e.g., `http://192.168.1.100:8501`)
2. **Cloud Deployment**: Deploy to Streamlit Cloud, Heroku, or other platforms
3. **Screenshots**: Take screenshots of configurations to share via email/Slack

## 🛠️ Technical Details

- **Framework**: Streamlit (Python web app framework)
- **Styling**: Custom CSS to match Salesforce Lightning Design System
- **Data Storage**: In-memory storage (resets on app restart)
- **Field Types Supported**: text, email, phone, picklist, date, number, currency, textarea, URL

## 🎨 What's Next

Based on your screenshots, we can:
- Add your specific objects and fields
- Match your exact field layouts
- Implement custom business logic
- Add validation rules
- Create custom page layouts

## 💡 Tips for Vibe Coders

- All code is well-commented to help you understand what's happening
- Each function has a clear purpose and documentation
- The app structure is modular - easy to modify one piece at a time
- CSS styling is separated for easy customization
- Use the browser's developer tools to inspect and modify styling

---

Ready to start? Just run `streamlit run app.py` and begin configuring your mock Salesforce!
