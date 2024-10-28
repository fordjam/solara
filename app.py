import solara
import pandas as pd
from datetime import date, datetime
import io
import openpyxl
from msoffcrypto.format.ooxml import OOXMLFile

# Sample client data
clients = ["Client A", "Client B", "Client C", "Client D"]

def df2excel(df, password=None):
    # Save the DataFrame to a BytesIO object (in-memory buffer)
    output = io.BytesIO()
    df.to_excel(output, index=False, engine="openpyxl")
    
    if password:
        # Encrypt the file in memory
        encrypted = io.BytesIO()
        output.seek(0)  # Reset to the start of the buffer
        file = OOXMLFile(output)
        file.encrypt(password, encrypted)
        encrypted.seek(0)
        return encrypted.getvalue()
    
    output.seek(0)
    return output.getvalue()

@solara.component
def ClientPicker():
    # State for selected client and date
    selected_client, set_selected_client = solara.use_state(clients[0])
    selected_date_str, set_selected_date_str = solara.use_state(date.today().strftime('%Y-%m-%d'))
    download_content, set_download_content = solara.use_state(None)

    # Save button handler
    def handle_save():
        try:
            # Convert date string to date object
            selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
            
            # Create a DataFrame with the selected client and date
            df = pd.DataFrame({
                "Client": [selected_client],
                "Date": [selected_date.strftime('%Y-%m-%d')]
            })
            
            # Generate encrypted Excel content
            file_content = df2excel(df, password="Passw0rd")
            
            # Set file content for download
            set_download_content(file_content)
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")

    # User Interface
    solara.Markdown("## Select a Client and Date")
    with solara.Row():
        solara.Select(label="Select a Client", values=clients, value=selected_client, on_value=set_selected_client)
        solara.InputText(label="Pick a Date (YYYY-MM-DD)", value=selected_date_str, on_value=set_selected_date_str)
    solara.Button(label="Save to Excel", on_click=handle_save)

    # Display download button if content is available
    if download_content:
        solara.FileDownload(
            label="Download Encrypted Excel File",
            filename="client_data_encrypted.xlsx",
            content=download_content,
        )

# Wrapper function named `Page` to serve as the entry point
@solara.component
def Page():
    ClientPicker()