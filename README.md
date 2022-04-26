# Django RSS READER


    
  <p align="center">
    <i>
A Instagram clone written in django :)
    </i>
  </p>
  
  <hr>
</p>

<p>


    A Rss reader created with Django, Postgres, celery, rabitmq , rest_framework and graphql
 <br>
</p>



<hr>

<h3>
⚙️ Config the project
</h3>

<p>
First you should make venv for this project.
So in the main root of project you should type this command in your Terminal or Console: 
</p>
<pre>
python -m venv venv
</pre>
<p>
Now you should activate your venv.
So in the main root of project you should type this command in your Terminal or Console: 
</p>
<b>
In Linux/macOS:
</b>
<pre>
source venv/bin/activate
</pre>
<b>
In Windows:
</b>
<pre>
venv/Scripts/activate
</pre>

<p>
After activating venv you should install the <b>requirements.txt</b> packages. So type this command in your Terminal or Console: 
</p>
<pre>
pip install -r requirements.txt
</pre>


<h5>
Configuration of project almost done.
</h5>

<hr>

<h3>
🏁 Run the project
</h3>
<p>
First of all, please enter the following command in the Terminal or Console to make sure the project is configured correctly:
</p>
<pre>
python manage.py check
</pre>
<p>
You should see This message:
  <strong>
    <i>
      "System check identified no issues (0 silenced)."
    </i>
  </strong>
  <br>
  If you see this message you should create your project database. So type this commands in Terminal or Console:
</p>

<pre>
python manage.py makemigrations
</pre>
<pre>
python manage.py migrate
</pre>

<p>
After creating the project database, you should run project. So type this command in Terminal or Console:
</p>
<pre>
python manage.py runserver
</pre>


### Fork
Fork and develop are free for everyone. Be sure I'll check your push requests out.

###### Made with :heart:
