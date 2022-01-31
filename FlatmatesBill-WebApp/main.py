from flask.views import MethodView
from wtforms import Form, StringField, SubmitField
from flask import Flask, render_template, request
from flatmates_bill import flat

app = Flask(__name__)


class HomePage(MethodView):

    def get(self):
        return render_template('index.html')


class BillFormPage(MethodView):

    def get(self):
        bill_form = BillForm()
        return render_template('bill_form_page.html', billform=bill_form)

    def post(self):
        billform = BillForm(request.form)
        amount = float(billform.amount.data)
        period = billform.period.data

        name1 = billform.name1.data
        days_in_house1 = int(billform.days_in_house1.data)

        name2 = billform.name2.data
        days_in_house2 = int(billform.days_in_house2.data)

        the_bill = flat.Bill(amount=amount, period=period)
        flatmate1 = flat.Flatmate(name=name1, days_in_house=days_in_house1)
        flatmate2 = flat.Flatmate(name=name2, days_in_house=days_in_house2)

        amount1 = round(flatmate1.pays(bill=the_bill, flatmate2=flatmate2), 2)
        amount2 = round(flatmate2.pays(bill=the_bill, flatmate2=flatmate1), 2)

        return render_template('bill_form_page.html',
                               result=True,
                               billform=billform,
                               name1=name1,
                               name2=name2,
                               amount1=amount1,
                               amount2=amount2)


class ResultPage(MethodView):
    def post(self):
        billform = BillForm(request.form)
        amount = float(billform.amount.data)
        period = billform.period.data

        name1 = billform.name1.data
        days_in_house1 = int(billform.days_in_house1.data)

        name2 = billform.name2.data
        days_in_house2 = int(billform.days_in_house2.data)

        the_bill = flat.Bill(amount=amount, period=period)
        flatmate1 = flat.Flatmate(name=name1, days_in_house=days_in_house1)
        flatmate2 = flat.Flatmate(name=name2, days_in_house=days_in_house2)

        amount1 = round(flatmate1.pays(bill=the_bill, flatmate2=flatmate2), 2)
        amount2 = round(flatmate2.pays(bill=the_bill, flatmate2=flatmate1), 2)

        return render_template('results.html', name1=name1, name2=name2, amount1=amount1, amount2=amount2)


class BillForm(Form):
    amount = StringField(label="Bill Amount: ", default="100")
    period = StringField(label="Bill Period: ", default="December 2020")

    name1 = StringField(label="Name: ", default="Jhon")
    days_in_house1 = StringField(label="Days in the house: ", default="20")

    name2 = StringField(label="Name: ", default="Marry")
    days_in_house2 = StringField(label="Days in the house: ", default="12")

    button = SubmitField("Calculate")


app.add_url_rule('/', view_func=HomePage.as_view('home_page'))
app.add_url_rule('/bill_form_page', view_func=BillFormPage.as_view('bill_form_page'))
# app.add_url_rule('/results', view_func=ResultPage.as_view('result_page'))

app.run(debug=True)
