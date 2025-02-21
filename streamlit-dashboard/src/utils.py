def format_data(data):
    # Function to format data for display in the Streamlit app
    formatted_data = []
    for item in data:
        formatted_data.append({
            'Column1': item[0],
            'Column2': item[1],
            'Column3': item[2],
        })
    return formatted_data

def generate_chart(data):
    # Function to generate a chart based on the provided data
    import matplotlib.pyplot as plt

    x = [item[0] for item in data]
    y = [item[1] for item in data]

    plt.figure(figsize=(10, 5))
    plt.bar(x, y)
    plt.xlabel('X-axis Label')
    plt.ylabel('Y-axis Label')
    plt.title('Sample Chart')
    plt.grid()
    plt.tight_layout()
    return plt