from models import db, Cupcake
from app import app

db.drop_all()
db.create_all()

c1 = Cupcake(flavor="Orange Cream Cheese",size="Small",rating="6.9",image="https://www.biscuitsandburlap.com/wp-content/uploads/2021/11/orange-cupcakes-1-735x1102.jpg")
c2 = Cupcake(flavor="Cookies n Cream",size="Large",rating="9.1",image="https://preppykitchen.com/wp-content/uploads/2017/12/oreo-cupcake-feature-768x1088.jpg")
c3 = Cupcake(flavor="Red Velvet",size="Small",rating="5.7",image="https://sallysbakingaddiction.com/wp-content/uploads/2014/10/Red-Velvet-Cupcakes-6.jpg")
c4 = Cupcake(flavor="Snickerdoodle",size="Large",rating="9.9",image="https://sugarspunrun.com/wp-content/uploads/2021/09/Snickerdoodle-Cupcakes-2-of-9-675x1013.jpg")
c5 = Cupcake(flavor="Chocolate",size="Medium",rating="8.2",image="https://sallysbakingaddiction.com/wp-content/uploads/2017/06/moist-chocolate-cupcakes-5-850x1276.jpg")

db.session.add_all([c1,c2,c3,c4,c5])
db.session.commit()