import solara
import ipyaggrid

def generate_mycolumn(data):
    return [{ 
        "field": key,
        "filter": True
    } for key in data[0].keys()] if data else []

@solara.component
def Page():

    data=[
    {"name":"dqwqw","age":12},
    {"name":"gerger","age":54},
    {"name":"jtjyt","age":65},
    {"name":"tyu","age":87},
    {"name":"mgh","age":6},
    {"name":"vsd","age":54},
    ]

    grid_options = {
        "columnDefs": generate_mycolumn(data),
        "defaultColDef":{
            "sortable": True
            },    
        "enableSorting":True,
        "enableFilter":True,
        "enableColResize":True
    }

    with solara.Column(margin=10):
        ipyaggrid.Grid.element(
            grid_data=data, 
            grid_options=grid_options,
            # AND SET THEME
            theme="ag-theme-material", 
            quick_filter=True
            )
