<h1>Installing the web application</h1>

<ol>
    <li> Construct a python virtual env in the base directory of the project via python3 -m venv venv </li>
    <li> pip install -r requirments.txt  </li>
    <li> 
        <h4> Build database with <h4>
        <ul>
            <li> flask db init </li>
            <li> flask db migrate -m "tables" </li>
            <li> flask db upgrade </li>
        </ul>
    </li>
    <li> Run using flask run (or flask run --debug) </li>
</ol>
