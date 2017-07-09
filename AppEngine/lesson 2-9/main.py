# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import webapp2

form = """
<form method="post">
	What is your birthday?
	<br>
	<label for="month">Month
    	<input type="text" name="month" value="%(month)s">
	</label>
	<label for="day">Day
    	<input type="text" name="day" value="%(day)s">
	</label>
	<label for="year">Year
    	<input type="text" name="year" value="%(year)s">
	</label>
    <div style="color: red">%(error)s</div>
	<br><br>
	<input type="submit">
</form>
"""

months = ['January',
            'February',
            'March',
            'April',
            'May',
            'June',
            'July',
            'August',
            'September',
            'October',
            'November',
            'December']

def valid_month(month):
    if month:
        upper = month.capitalize()
        
        if upper in months:
            return upper

    return None

def valid_day(day):
    if (day.isdigit()):
        num = int(day)
        if num > 0 and num <= 31:
            return num
            
    return None

def valid_year(year):
    if year.isdigit():
        num = int(year)
        if num >= 1900 and num <= 2020:
            return num
            
    return None

def escape_html(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


class MainPage(webapp2.RequestHandler):
    def write_form(self, error="", month="", day="", year=""):
        self.response.out.write(form % {
            "error": error, 
            "month": escape_html(month), 
            "day": escape_html(day), 
            "year": escape_html(year)})

    def get(self):
        self.write_form()

    def post(self):
        month = self.request.get("month")
        day = self.request.get("day")
        year = self.request.get("year")

        v_month = valid_month(month)
        v_day = valid_day(day)
        v_year = valid_year(year)

        if not (v_month and v_day and v_year):
            self.write_form("That doesn't look valid to me friend.", month, day, year)
        else:
            self.redirect("/thanks")

class ThanksHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("Thanks! That's a totally valid day!")

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ("/thanks", ThanksHandler)
], debug=True)