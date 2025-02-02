# Virtual Environment & Streamlit App Setup

## Running the Virtual Environment  

1. Open the terminal or command prompt.  
2. Navigate to the directory where you want to create the virtual environment.  
3. Run the command:  

   ```sh
   python -m venv myenv  
   ```
   (Replace myenv with your preferred environment name.)

4. Activate the venv
    ### On Windows
    ```sh
    .\myenv\Scripts\activate  
    ```
    ### On MacOs/Linux
    ```
    source myenv/bin/activate  
    ```

================================================================================================

## Running Streamlit app

1. Ensure the virtual environment is activated.
2. Run the following command:
    ```
    streamlit run app.py 
    ```