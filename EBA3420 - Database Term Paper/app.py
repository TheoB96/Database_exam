from distutils.debug import DEBUG
import sqlite3
from flask import Flask, render_template, request

# Database path
DATABASE = 'database/database.db'



app = Flask(__name__)
app.config['SECRET_KEY'] = 'dd421f27d441f27567d441f2b6176a'

# Front page
@app.route('/', methods = ['POST', 'GET'])
def index():

    # Connect to db
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    # Get data from frompage info from db
    c.execute("SELECT cinema_viewings.program_id, movie.movie_title, cinema_viewings.date_time, auditorium.auditorium_name, cinema_viewings.ticket_price FROM cinema_viewings JOIN movie USING(movie_id) JOIN auditorium USING(auditorium_id) ORDER BY date_time ASC")
    data = c.fetchall()

    # Get the first 5 films and request more if button load more is pressed
    if request.method == 'POST':
        conn.close()
        return render_template("index.html", data = data)
    else:
        conn.close()
        return render_template("index.html", data = data[0:5])

#Detail page
@app.route('/<program_id>', methods = ['POST', 'GET'])
def detail(program_id):

    # Reset the satus code(used for error and success messages)
    status_code = 0

    # Connect to db
    conn = sqlite3.connect(DATABASE)  
    c = conn.cursor()
    
    # Get info about the right cinema viewing
    c.execute('SELECT movie_title, movie_description FROM cinema_viewings JOIN movie USING(movie_id) WHERE program_id = %s' % program_id)
    movie_info = c.fetchall()

    # Get the audutorium info and capacity from right cinema viewing
    c.execute('SELECT date_time, auditorium_name, auditorium_capacity, ticket_price FROM cinema_viewings JOIN auditorium USING(auditorium_id) WHERE program_id = %s' % program_id)
    cinema_info = c.fetchall()

    # Get data for the table inside detail page about the right cinema viewing
    c.execute('SELECT order_id, last_name, first_name, email, phone_number, tickets FROM booking JOIN users USING(user_id) WHERE program_id = %s ORDER BY last_name' % program_id)
    ticket_orders = c.fetchall()

    # Get all registered tickets and the auditorium capacity
    c.execute('SELECT SUM(tickets), auditorium_capacity FROM booking JOIN cinema_viewings USING(program_id) JOIN auditorium USING(auditorium_id) WHERE program_id = %s' % program_id)
    ticket_availability = c.fetchall()

    # Calculate the tickets left
    if ticket_availability[0][0] is not None:
        ticket_left = ticket_availability[0][1] - ticket_availability[0][0]
    else:
        ticket_left = cinema_info[0][2]

    # If the submit button on the form is pressed
    if request.method == 'POST':

        # Get email and ticket number for the form
        email = request.form['email']
        tickets = int(request.form['tickets'])

        # Get all email from the system with user id 
        c.execute('SELECT user_id, email FROM users')
        all_emails = c.fetchall()

        # Get order_id, email, tickets from the right booking
        c.execute('SELECT order_id, email, tickets FROM booking JOIN users USING(user_id) WHERE program_id = %s' % program_id)
        all_orders = c.fetchall()

        # Check if the current ticket left is over 0 and if the user is not ordering over the avaible tickets left
        if ticket_left > 0 and ticket_left >= tickets:

            # Go through every email in the user table
            for emails in all_emails:
                # If the form email adress is present in user table then..
                if email in emails:

                    # Make a small list
                    correct_order = []

                    # Go through every order
                    for user_order in all_orders:

                        # If the order contains the form email, append order id and tickets back to small list
                        if user_order[1] == email:
                            correct_order.append(user_order[0])
                            correct_order.append(user_order[2])

                    # Check if the correct order contains any values
                    if correct_order:

                        # Calculate the additional tickets + the old tickets on the order/booking
                        new_tickets = tickets + correct_order[1]

                        # Success! Update the order with the additional tickets
                        c.execute('UPDATE booking SET tickets = %s WHERE order_id = %s' % (new_tickets, correct_order[0]))
                        

                        # Get the order info, used for the success message. 
                        c.execute('SELECT last_name, first_name, email, tickets FROM booking JOIN users USING(user_id) WHERE program_id = %s AND order_id == %s' % (program_id, correct_order[0]))
                        order_info = c.fetchall()

                        # Update the tickets available
                        ticket_left = ticket_left - tickets

                        # Get data for the table inside detail page about the right cinema viewing, again
                        c.execute('SELECT order_id, last_name, first_name, email, phone_number, tickets FROM booking JOIN users USING(user_id) WHERE program_id = %s ORDER BY last_name' % program_id)
                        ticket_orders = c.fetchall()
                        
                        # Send an success message for the user that the order has been updated
                        status_code = 4
                        conn.commit()
                        conn.close()
                        return render_template('detail-page.html', movie_info=movie_info, ticket_orders=ticket_orders, cinema_info=cinema_info, ticket_left=ticket_left, status_code=status_code, order_info=order_info, ticket_add = tickets)

                    # If the small list dont contain any values
                    else:
                        # Success! Email could not be found under this booking, user have been added to this booking.
                        # Create new order id
                        c.execute('SELECT MAX(order_id) FROM booking')
                        order_id = c.fetchall()
                        if order_id[0][0] is not None:
                            order_id = order_id[0][0] + 1
                        else:
                            order_id = 1

                        # Insert new values into the booking table
                        c.execute('INSERT INTO booking VALUES (%s, %s, %s, %s)' % (order_id, program_id, emails[0], tickets))
                       

                        # Get the order info, used for the Success message. 
                        c.execute('SELECT last_name, first_name, email, tickets FROM booking JOIN users USING(user_id) WHERE program_id = %s AND user_id == %s' % (program_id, emails[0]))
                        order_info = c.fetchall()

                        # Update the tickets available
                        ticket_left = ticket_left - tickets

                        # Get data for the table inside detail page about the right cinema viewing, again
                        c.execute('SELECT order_id, last_name, first_name, email, phone_number, tickets FROM booking JOIN users USING(user_id) WHERE program_id = %s ORDER BY last_name' % program_id)
                        ticket_orders = c.fetchall()

                        #Send an sukksess message for the user that the order has been added
                        status_code = 3
                        conn.commit()
                        conn.close()
                        return render_template('detail-page.html', movie_info=movie_info, ticket_orders=ticket_orders, cinema_info=cinema_info, ticket_left=ticket_left, status_code=status_code, order_info=order_info, ticket_add = tickets)
                else:
                    #Return satuscode 2: Count find email address in the system
                    status_code = 1
        else:
            # Return satuscode 2: No tickets left 
            status_code = 2
            
        return render_template('detail-page.html', movie_info=movie_info, ticket_orders=ticket_orders, cinema_info=cinema_info, ticket_left=ticket_left, status_code=status_code)
    
    else:
        conn.close()
        return render_template('detail-page.html', movie_info=movie_info, ticket_orders=ticket_orders, cinema_info=cinema_info, ticket_left=ticket_left, status_code=status_code)    
    

if __name__ == '__main__':
    app.run(debug=True, threaded=True)