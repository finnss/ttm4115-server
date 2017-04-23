# ttm4115-server
This gon be gud!

**This server has the following tasks:**
- To receive data from our Raspberry Pi
- To store that data in our database
- To implement logic checking whether that data is within legal levels based on config data from the database
- To initialize sending of an SMS to interested users if data is not within legal levels

**Installation guide**
1. `git clone https://github.com/finnss/ttm4115-server.git`
2. Navigate to the cloned directory
3. `pip install --upgrade virtualenv` (assuming you have pip)
4. `virtualenv -p python3 venv`
5. `source venv/bin/activate`
6. `pip install django`
7. `pip install paho`
8. `pip install slackclient`
9. `python manage.py migrate`
10. `python manage.py runserver`
11. Should be running at `localhost:8000`!