import geo_ride

app = geo_ride.create_app()

if __name__ == '__main__':
    app.run(debug=True,port=5000,host='0.0.0.0')
