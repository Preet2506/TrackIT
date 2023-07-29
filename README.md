# Tracking  
***   
### Requirements and Set Up
***
First of all downlaod **Flask** using the command:-  
`pip install flask`  

Install playwright  
```
pip install playwright 
playwright install
```
Second command is necessary in order to install the playwright libraries.  
Playwright is a library used for automating web browsers to perform web scraping. It also supports headless execution.  

Install **tmux** to run the app in background  

***
### Flask app

create a basic flask app:-
``` 
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, world!"

if __name__ == "__main__":
    app.run(debug=True)

```
In the above code `hello()` is our funtion where we will call our respective couriers and create funtion names as per courier names.  
The `@app.route("/")` will contain the path our courier.  

For example , let's take dhl:-  
```
@app.route("/dhl/<int:tkno>")
def dhl(tkno):
    data=trackDHL(tkno)
    return data
```
In the above code tkno is the awb number and data is the data returned by the trackDHL funtion where the data is scraped from the DHL website.  

If we have to run our app on custom url and port , it can be mentioned in `app.run` , for example:-  
```
if __name__ == "__main__":
    app.run(debug=True,host="164.90.217.128" , port="5001")
```

***
### Scraping

Now for scraping the data from the website we will be using playwright.  
First of all we will create a funtion which will return the scraped data.  
In this we will create a instance of playwright API and establish a connection to the browser.  
`with sync_playwright() as pl:`  
in this instance our complete data will be extracted.  

To open a browser we write command:-  
`browser = pl.chromium.launch(headless=False , slow_mo=800 ,)`   
Here , headless is used to define either we want a headless browser or not and `slow_mo` defines the pace of automation.  

Then we create a context of the browser as  
`context = browser.new_context()`  
and if we want to add headers , they can be added in it as  
``` 
extra_http_headers={
            "user-agent" : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
        }
```
And this `extra_http_headers` would go in context.  

Then we would create a new page as  
`page = context.new_page()` 

Then we can hit the link of the courier website by `page.goto()` method.

The different command to perform different operation in playwright are:-  
- `page.click()` :- to click a button or link  
- `page.fill('path',value)` :- to fill any value in any input field.
- `page.wait_for_selector()` :- wait till any selector appears.  
- `page.inner_html()` :- to extract the html content and this should be assigned to a variable.  
- `page.text_content()` :- to extract the text content and this should be assigned to a variable.  
- `page.close()` :- to close the page opened.  
- `page.screenshot()` :- to take the screenshot of any page  

***
### Semaphore
We are using `Semaphores` to manage the load and limit the number of browsers opened at one time to a specific upper limit.  
To define the semophore we write :- `browser_semaphore = Semaphore(10)`.  
Now to acquire a semaphore we write :- `browser_semaphore.acquire()`  
and to release we write :- `browser_semaphore.release()`  
To chech the number of semophores available :- `browser_semaphore._value`